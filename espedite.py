#! /usr/bin/env python
import itertools
from multiprocessing import Pool
from string import ascii_lowercase

import whois

import util.opt_parser as parser
from util.toolkit import log, PermutationIterator, start_busy_indicator, stop_busy_indicator

if __name__ == '__main__':

    # Begin the Busy indicator
    bi = start_busy_indicator("")

    def calculate_permutations(character_list, length):
        counter = 0
        for p in itertools.permutations(character_list, length):
            counter += 1

        return counter


    def run_name(dn):
        try:
            whois.query(dn)
            log.debug("[TAKEN] " + dn)
        except Exception:
            log.info("[FREE] " + dn)


    log.info("Permutations are " + str(calculate_permutations(ascii_lowercase, int(parser.options.length))))

    # Setup pool
    p = Pool(int(parser.options.workers))

    for e in PermutationIterator(ascii_lowercase, int(parser.options.length)):
        domain_name = str("".join(e) + parser.options.tld)
        result = None

        log.debug("Trying: " + domain_name)

        try:
            # Give it to an available worker
            p.apply(run_name, args=(domain_name,))

        except KeyboardInterrupt:
            p.terminate()


    # End the busy indicator
    stop_busy_indicator(bi)

    # Salute!
    log.info("Bye bye! :-)")
