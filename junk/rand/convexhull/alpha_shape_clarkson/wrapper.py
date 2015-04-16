#!/usr/bin/python -O

import sys, os
import subprocess
import tempfile

hull_path = "./hull.exe"

def get_alpha_shape(points):
    # Write points to tempfile
    tmpfile = tempfile.NamedTemporaryFile(delete=False)
    for point in points:
        tmpfile.write("%0.7f %0.7f\n" % point)
    tmpfile.close()

    # Run hull
    command = "%s -A -m1000000 -oN < %s" % (hull_path, tmpfile.name)
    print >> sys.stderr, "Running command: %s" % command
    retcode = subprocess.call(command, shell=True)
    if retcode != 0:
        print >> sys.stderr, "Warning: bad retcode returned by hull.  Retcode value:" % retcode
    os.remove(tmpfile.name)

    # Parse results
    results_file = open("hout-alf")
    results_file.next() # skip header
    results_indices = [[int(i) for i in line.rstrip().split()] for line in results_file]
#    print "results length = %d" % len(results_indices)
    results_file.close()
    os.remove(results_file.name)

    return [(points[i], points[j]) for i,j in results_indices]

if __name__ == "__main__":
    points = [tuple([float(i) for i in line.rstrip().split()]) for line in sys.stdin]
    for point_i, point_j in get_alpha_shape(points):
        sys.stdout.write("%0.7f,%0.7f\t%0.7f,%0.7f\n" % (point_i[0], point_i[1], point_j[0], point_j[1]))
    sys.exit(0)
