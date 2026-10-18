"""Generate draft enclosure STL files in millimetres, using only Python stdlib."""
from pathlib import Path
from collections import Counter
import math
import struct

ROOT = Path(__file__).resolve().parent

def ring(w, d, z):
    return [(-w/2,-d/2,z),(w/2,-d/2,z),(w/2,d/2,z),(-w/2,d/2,z)]

def build(name, sections):
    vertices = [p for section in sections for p in ring(*section)]
    faces = [(0,2,1),(0,3,2)]
    for k in range(len(sections)-1):
        for i in range(4):
            a,b,c,d = 4*k+i,4*k+(i+1)%4,4*(k+1)+(i+1)%4,4*(k+1)+i
            faces.extend([(a,b,c),(a,c,d)])
    n=4*(len(sections)-1)
    faces.extend([(n,n+1,n+2),(n,n+2,n+3)])
    edges=Counter(tuple(sorted((f[i],f[(i+1)%3]))) for f in faces for i in range(3))
    assert all(count==2 for count in edges.values()), 'Non-manifold edge'
    directed=Counter((f[i],f[(i+1)%3]) for f in faces for i in range(3))
    assert all(directed[(b,a)]==count for (a,b),count in directed.items())
    volume=0
    with (ROOT/name).open('wb') as out:
        out.write(b'Draft audio receiver enclosure; units mm'.ljust(80,b'\0'))
        out.write(struct.pack('<I',len(faces)))
        for face in faces:
            a,b,c=[vertices[i] for i in face]
            u=[b[i]-a[i] for i in range(3)]
            v=[c[i]-a[i] for i in range(3)]
            normal=[u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]]
            length=math.sqrt(sum(x*x for x in normal))
            assert length>0
            normal=[x/length for x in normal]
            volume += (a[0]*(b[1]*c[2]-b[2]*c[1])+a[1]*(b[2]*c[0]-b[0]*c[2])+a[2]*(b[0]*c[1]-b[1]*c[0]))/6
            out.write(struct.pack('<12fH',*normal,*a,*b,*c,0))
    assert volume>0
    print(f'{name}: {len(faces)} triangles, closed oriented mesh, volume {volume:.1f} mm^3')

# Base: 2 mm floor and walls; 96 x 71 x 26 mm open cavity.
build('receiver_base.stl',[(100,75,0),(100,75,28),(96,71,28),(96,71,2)])
# Print lid flat-side down. Flip over for assembly. Skirt clearance: 0.3 mm/side.
build('receiver_lid.stl',[(100,75,0),(100,75,2),(95.4,70.4,2),(95.4,70.4,5),(93,68,5),(93,68,2)])
