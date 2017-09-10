
newtype Cont r a = Cont { runCont :: (a -> r) -> r }

instance Monad Cont r where
    return :: a -> Cont r a
    return a = Cont $ \c -> c a
    (>>=) :: Cont r a -> (a -> Cont r b) -> Cont r b
    m >>= k = Cont $ \b -> runCont m (\a -> runCont (k a) b)

callCC :: ((a -> Cont r b) -> Cont r a) -> Cont r a
callCC f = Cont $ \h -> runCont (f (\a -> Cont $ \_ -> h a)) h

-- ref: https://zhuanlan.zhihu.com/p/25749077