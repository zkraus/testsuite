#!/bin/awk -f

BEGIN {
    i=0
}

/^[+-]+ b\// {
    gsub(/^[+-]+ b\//, "")
    test_file = $0

}

/+def test_/{
    gsub(/^+def /, "")
    gsub(/\(.*$/, "")
    tests[i++]=test_file"::"$0
}

END {
    oneliner = ""
    print "Tests added:"
    for (item in tests) {
        print "* `" tests[item] "`"
        oneliner = oneliner "" tests[item]
    }
    print ""
    print "# Verification Steps"
    print "```poetry run pytest -vv " oneliner "```"
}