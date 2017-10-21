import Data.Dynamic
import Data.Maybe
 
-- 
-- A list of dynamic 
--
hlist :: [Dynamic]
hlist = [ toDyn "string"
        , toDyn (7 :: Int)
        , toDyn (pi :: Double)
        , toDyn 'x'
        , toDyn ((), Just "foo")
        ]
 
dyn :: Dynamic 
dyn = hlist !! 1
 
--
-- unwrap the dynamic value, checking the type at runtime
--
v :: Int
v = case fromDynamic dyn of
        Nothing -> error "Type mismatch"
        Just x  -> x

{-# LANGUAGE ExistentialQuantification #-}
--
-- An existential type encapsulating types that can be Shown
-- The interface to the type is held in the show method dictionary
--
-- Create your own typeclass for packing up other interfaces
--
data Showable = forall a . Show a => MkShowable a
    
--
-- And a nice existential builder
--
pack :: Show a => a -> Showable
pack = MkShowable
    
--
-- A heteoregenous list of Showable values
--
hlist :: [Showable]
hlist = [ pack 3
        , pack 'x'
        , pack pi
        , pack "string"
        , pack (Just ()) ]
    
--
-- The only thing we can do to Showable values is show them
--
main :: IO ()
main = print $ map f hlist
    where
        f (MkShowable a) = show a
    
{-
    
*Main> main
["3","'x'","3.141592653589793","\"string\"","Just ()"]
    
-}