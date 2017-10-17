; Regular order: first expand test and then 0 = 0
; Application order: first evaluate p and then loop
(define (p) (p))
(define (test x y)
    (if (= x 0)
         0
         y))