#!/bin/awk -f
BEGIN   {
#    print "--BEGIN " $FILENAME
#    print FILENAME
    print "Test case,asserts"
}

#BEGINFILE {print FILENAME}

/^def test_/        {
    name = $2
    gsub(/\(.*$/, "",name)
    test_name = FILENAME"::"name
    test_cases[test_name] = 0
#    print test_name
}

/assert/ {
    test_cases[test_name]++
}


END     {

    for (i in test_cases) {
        print i "," test_cases[i]
    }

}
