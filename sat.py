def read_cnf(file):
    f = open(file, "r")
    l = "1"
    cnf = []
    while l:
        l = f.readline()
        if len(l) > 0:
            ps = []
            for i in l:
                if i is not '\n':
                    ps.append(0 if i is '0' else 1 if i is '1' else 2)
            cnf.append(ps)
    f.close()
    return cnf

def print_cnf(cnf):
    prt = ""
    for c in range(len(cnf)):
        prt = prt + "("
        ps = []
        for p in range(len(cnf[c])):
            if cnf[c][p] is not 2:
                ps.append("{}P{}".format("~" if cnf[c][p] is 0 else "", p))
        s = ""
        for p in range(len(ps)):
            s = s + ps[p]
            if p < len(ps) - 1:
                s = s + " v "
        prt = prt + s + ")"
        if c < len(cnf) - 1:
            prt = prt + " ^ "
    print(prt)

def print_res_vec(res_vec):
    prt = ""
    for r in res_vec:
        prt = prt + "P{} = {}\n".format(r[0], "T" if r[1] is 1 else "F")
    print(prt)
def print_res(cnf, res):
    print_res_vec(res)
    prt = ""
    for c in range(len(cnf)):
        prt = prt + "("
        ps = []
        for p in range(len(cnf[c])):
            if cnf[c][p] is not 2:
                d = True
                r = (0,)
                for rr in res:
                    if rr[0] is p:
                        d = False
                        r = rr
                ps.append("d" if d else "T" if r[1] is cnf[c][p] else "F")
        s = ""
        for p in range(len(ps)):
            s = s + ps[p]
            if p < len(ps) - 1:
                s = s + " v "
        prt = prt + s + ")"
        if c < len(cnf) - 1:
            prt = prt + " ^ "
    print(prt)

def eval_res(cnf, res):
    cval = []
    for c in range(len(cnf)):
        is_c_t = False
        for p in range(len(cnf[c])):
            if cnf[c][p] is not 2:
                r = None
                for rr in res:
                    if rr[0] is p:
                        r = rr
                if r is not None:
                    is_c_t = True if r[1] is cnf[c][p] else is_c_t
        cval.append(is_c_t)
    return cval

def solve(cnf, result_vector, last_len = None):
    # end condition
    if len(cnf) is last_len or len(cnf) is 0:
        return
    else:
        last_len = len(cnf)

    # find literal with maximum effect and minimum side-effect
    pn = len(cnf[0])
    cn = len(cnf)
    pe = [0 for i in range(3*pn)]
    for c in cnf:
        for p in range(pn):
            if c[p] is 0:
                pe[p*3] = pe[p*3] + 1
            elif c[p] is 1:
                pe[p*3 + 1] = pe[p*3 + 1] + 1
            elif c[p] is 2:
                pe[p*3 + 2] = pe[p*3 + 2] + 1
    
    maxp = 0 # maximum effect
    maxps = 0 if pe[1] < pe[0] else 1
    maxp2 = pe[2] # minimum side-effect
    for i in range(pn):
        p0 = pe[i*3]
        p1 = pe[i*3 + 1]
        p2 = pe[i*3 + 2]
        mps = 0 if p0 > p1 else 1
        mp = p0 if mps is 0 else p1
        if mp >= pe[maxp*3 + maxps]:
            if p2 > maxp2 or mp > pe[maxp*3 + maxps]:
                maxp = i
                maxps = mps
                maxp2 = p2

    # found one
    result_vector.append((maxp, maxps))

    # cut the cnf
    ncnf = []
    for c in cnf:
        if c[maxp] is not maxps:
            ncnf.append([p for p in c])
    for c in ncnf:
        c[maxp] = 2

    # solve new cnf
    solve(ncnf, result_vector, last_len)



# driver
import sys
from random import random
def rnd():
    r = random()
    return 0 if r < 0.33 else 1 if r < 0.66 else 2
def fill(file, n, m):
    f = open(file, "w+")
    for i in range(n):
        s = ""
        for j in range(m):
            s = s + str(rnd())
        f.write(s + '\n')
    f.close()
if __name__ == "__main__":
    if len(sys.argv) is 4:
        fill(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
    else:
        cnf = read_cnf(sys.argv[1])
        res_vec = []
        solve(cnf, res_vec)
        if len(cnf) <= 5 or len(cnf[0]) <= 7:
            print_cnf(cnf)
            print_res(cnf, res_vec)
        else:
            # eval and print how many clauses where true
            eval_res(cnf, res_vec)