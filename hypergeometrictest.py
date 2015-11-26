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

    source: https://www.biostars.org/p/66729/
    Other interesting links about hypergeometric tests: 404 not found

    """
    return stats.hypergeom.sf(subset_condition_count - 1,
                              pop_size, pop_condition_count, subset_size)

if __name__ == '__main__':
    import sys
    print(phyper(int(sys.argv[1]), int(sys.argv[2]),
                 int(sys.argv[3]), int(sys.argv[4])))
