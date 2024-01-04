import numpy as np
import mpmath as mp
from scipy.sparse import coo_matrix, csr_matrix

from neutralocean.lib import aggsum
from neutralocean.bfs import bfs_conncomp1
from neutralocean.grid.graph import edges_to_graph
from neutralocean.ppinterp import make_pp

# def _linprob(s, t, p, ds, dt, dds, ddt, M, grid, eos, vc, DERIV):
def omegapp(s, t, p, M, grid, eos_s_t):
    """Calculate the Jacobian and Hessian of E"""
    N = len(M)

    # `remap` changes from linear indices (0, 1, ..., ni*nj-1) for the entire
    # space (including land), into linear indices (0, 1, ..., N-1) for the
    # current connected component
    remap = np.full(p.size, -1, dtype=int)
    remap[M] = np.arange(N)

    # Select a subset of edges, namely those between two "wet" casts that are
    # in this connected component.
    a, b = grid["edges"]
    ge = (remap[a] >= 0) & (remap[b] >= 0)  # good edges
    a, b = a[ge], b[ge]

    fac = grid["distratio"][ge]
    dperp = grid["distperp"][ge]
    areaG = grid["dist"][ge] * dperp
    
    sa, ta, pa = (x[a] for x in (s, t, p))
    sb, tb, pb = (x[b] for x in (s, t, p))

    rs, rt = eos_s_t(0.5 * (sa + sb), 0.5 * (ta + tb), 0.5 * (pa + pb))
    
    Δs = sb - sa
    Δt = tb - ta
    e = (rs * Δs + rt * Δt)
    
    B = e * 100

    # e = ntp_epsilon_errors(s, t, p, (a, b), eos_d3)
    # sa, ta, pa = (graph_binary_fcn(edges, x, avg1) for x in (s, t, p))
    # Δs, Δt = (graph_binary_fcn(edges, x, dif1) for x in (s, t))

    Hab = fac
    Hba = fac

    # Henceforth we only refer to nodes in the connected component, so remap edges now
    a, b = remap[a], remap[b]

    # For omega, the matrix is the negative Laplacian.  For uniform geometry,
    # this simply counts the number of edges incident upon each node.  For
    # rectilinear grids, this value will be 4 for a typical node, but can be
    # less near boundaries of the connected component.  This is achieved by
    #   diag = aggsum(fac, a, N) + aggsum(fac, b, N)
    # and then using (-fac) on the off-diagonal.
    # For ONS, the matrix is the Hessian of E.
    # Diagonal of Hessian is
    # diag[m] = 
    #   = ∑_{n ∈ N(m)} Bₘₙ
    #   =   ∑_{j=1}^E  δ_{m, aⱼ} B_{m, bⱼ} + ∑_{j=1}^E  δ_{m, bⱼ} B_{m, aⱼ}
    #   =   ∑_{j=1}^E  δ_{m, aⱼ} B_{m, bⱼ} - ∑_{j=1}^E  δ_{m, bⱼ} B_{aⱼ, m}
    #   =   np.sum(Bab[a == m]) - np.sum(Bab[b == m])
    #   =   aggsum(Bab, a, N)[m] - aggsum(Bab, b, N)[m]
    diag = (
        aggsum(-fac + B * dperp - 0.5 * B**2 * areaG, a, N) +
        aggsum(-fac - B * dperp - 0.5 * B**2 * areaG, b, N)
    )

    # Build the rows, columns, and values of the sparse matrix
    r = np.concatenate((a, b, np.arange(N)))
    c = np.concatenate((b, a, np.arange(N)))
    v = np.concatenate((Hab, Hba, diag))

    return v, r, c


# Pre-calculate grid adjacency needed for Breadth First Search
p = z_omega
P = Z
M0 = I0

grid1 = grid.copy()
grid1["dist"][:] = 1.0
grid1["distperp"][:] = 1.0
grid1["distratio"][:] = 1.0

interp_name = "pchip"
I2 = make_pp(interp_name, "u", out="interp", num_dep_vars=2)
s, t = I2(p, P, S, T, 0)

N = np.prod(p.shape)  # number of nodes (water columns)
edges = grid1["edges"]
graph = edges_to_graph(edges, N)
good = np.isfinite(mp.fp.matrix(p))
M = bfs_conncomp1(graph.indptr, graph.indices, M0, good)
v, r, c = omegapp(s, t, p, M, grid1, eos_s_t)

Hmp = mp.matrix(len(M), len(M))
for i in range(len(r)):
    Hmp[r[i], c[i]] += v[i]

Hnp = csr_matrix((np.float64(v), (r, c)), shape=(len(M), len(M)))
    
Es, Qs = mp.eigsy(Hmp)
Esnp = np.array(mp.fp.matrix(Es))  # convert to np.array of floats
i = int(np.argmin(abs(Esnp)))  # index to smallest abs eigenvalue
eigval = Es[i]
eigvec = Qs[:, i]

# print(Hnp[:,5].toarray())
print(eigval)