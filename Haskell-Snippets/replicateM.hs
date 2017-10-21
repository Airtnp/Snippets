-- https://www.reddit.com/r/haskell/comments/77okk2/generalization_of/
((,) <$>) >>= (<*>) -- replicateM 2
((,,) <$>) >>= (<*>) >>= (<*>) -- replicate M 3
((,,,) <$>) >>= (<*>) >>= (<*>) >>= (<*>)