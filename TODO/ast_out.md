Module (
  body = [
    ClassDef (
      name = 'A',
      bases = [],
      keywords = [],
      body = [
        FunctionDef (
          name = '__init__',
          args = arguments (
            args = [
              arg (
                arg = 'self',
                annotation = None
              ),
              arg (
                arg = 'n',
                annotation = None
              )
            ],
            vararg = None,
            kwonlyargs = [],
            kw_defaults = [],
            kwarg = None,
            defaults = []
          ),
          body = [
            Assign (
              targets = [
                Attribute (
                  value = Name (
                    id = 'self',
                    ctx = Load ()
                  ),
                  attr = 'n',
                  ctx = Store ()
                )
              ],
              value = Name (
                id = 'n',
                ctx = Load ()
              )
            )
          ],
          decorator_list = [],
          returns = None
        )
      ],
      decorator_list = []
    ),
    FunctionDef (
      name = 'fac',
      args = arguments (
        args = [
          arg (
            arg = 'n',
            annotation = None
          )
        ],
        vararg = None,
        kwonlyargs = [],
        kw_defaults = [],
        kwarg = None,
        defaults = []
      ),
      body = [
        Assign (
          targets = [
            Name (
              id = 'a',
              ctx = Store ()
            )
          ],
          value = Call (
            func = Name (
              id = 'A',
              ctx = Load ()
            ),
            args = [
              Name (
                id = 'n',
                ctx = Load ()
              )
            ],
            keywords = []
          )
        ),
        Return (
          value = BinOp (
            left = Attribute (
              value = Name (
                id = 'a',
                ctx = Load ()
              ),
              attr = 'n',
              ctx = Load ()
            ),
            op = Mult (),
            right = Call (
              func = Name (
                id = 'fac',
                ctx = Load ()
              ),
              args = [
                BinOp (
                  left = Name (
                    id = 'n',
                    ctx = Load ()
                  ),
                  op = Sub (),
                  right = Num (
                    n = 1
                  )
                )
              ],
              keywords = []
            )
          )
        )
      ],
      decorator_list = [],
      returns = None
    ),
    Assign (
      targets = [
        Name (
          id = 'n',
          ctx = Store ()
        )
      ],
      value = Call (
        func = Name (
          id = 'fac',
          ctx = Load ()
        ),
        args = [
          Num (
            n = 10
          )
        ],
        keywords = []
      )
    ),
    AugAssign (
      target = Name (
        id = 'n',
        ctx = Store ()
      ),
      op = Add (),
      value = Call (
        func = Name (
          id = 'fac',
          ctx = Load ()
        ),
        args = [
          Num (
            n = 20
          )
        ],
        keywords = []
      )
    ),
    Assign (
      targets = [
        Name (
          id = 'm',
          ctx = Store ()
        )
      ],
      value = List (
        elts = [
          Name (
            id = 'n',
            ctx = Load ()
          )
        ],
        ctx = Load ()
      )
    ),
    Assign (
      targets = [
        Name (
          id = 'k',
          ctx = Store ()
        )
      ],
      value = Subscript (
        value = Name (
          id = 'm',
          ctx = Load ()
        ),
        slice = Index (
          value = BinOp (
            left = Name (
              id = 'n',
              ctx = Load ()
            ),
            op = Add (),
            right = Subscript (
              value = Name (
                id = 'm',
                ctx = Load ()
              ),
              slice = Slice (
                lower = Num (
                  n = 0
                ),
                upper = Num (
                  n = 1
                ),
                step = Num (
                  n = 2
                )
              ),
              ctx = Load ()
            )
          )
        ),
        ctx = Load ()
      )
    )
  ]
)
