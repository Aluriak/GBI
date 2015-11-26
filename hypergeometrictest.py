from __future__ import print_function
import scipy.stats as stats


def phyper(pop_size, pop_condition_count,
           subset_size, subset_condition_count):
    """Return the likelihood of get a number of elements with a condition
    in a population subset.

    pop_size: total number of elements in population
    pop_condition_count: total number of elements with condition in population
    subset_size: number of element in subset
    subset_condition_count: number of element with condition in subset

    A loss of precision is expected for big values.

    sources:
        - https://www.biostars.org/p/66729/
        - http://stackoverflow.com/questions/6594840/what-are-equivalents-to-rs-phyper-function-in-python
        - http://stackoverflow.com/questions/32859103/python-scipys-hypergeometric-test-not-equal-to-r-or-sas
    Other interesting links about hypergeometric tests: 404 not found

    """
    return stats.hypergeom.sf(subset_condition_count - 1,  # without -1, results are generally false
                              pop_size, pop_condition_count, subset_size)

if __name__ == '__main__':
    import sys
    print(phyper(int(sys.argv[1]), int(sys.argv[2]),
                 int(sys.argv[3]), int(sys.argv[4])))
