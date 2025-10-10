find . -name "*py" |\
 grep -E "test_[a-zA-Z1-9_]+\.py" |\
  xargs awk -f awk_assert_counter.awk

