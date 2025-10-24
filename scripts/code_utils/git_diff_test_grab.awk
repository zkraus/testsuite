#!/bin/awk -f

BEGIN {
    i=0
}

/^[+-]+ b\// {
    gsub(/^[+-]+ b\//, "")
    test_file = $0

}

/^+def test_/{
    gsub(/^+def /, "")
    gsub(/\(.*$/, "")
    tests[i++]=test_file"::"$0
}

END {
    oneliner = ""
    if (length(tests) > 0) {
#        print "Tests added:"
        for (item in tests) {
#            print "* `" tests[item] "`"
            oneliner = oneliner " " tests[item]
        }
#        print ""
#        print "# Verification Steps"
        print "poetry run pytest -vv " oneliner
    } else {
#        print "No new tests added"
    }



}