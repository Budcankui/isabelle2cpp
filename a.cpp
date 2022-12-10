
class bAA {
    struct _True {};
    struct _False {};
    std::variant< _True, _False > value_;
public:
    bAA() = default; 
    bAA(_True p) { value_ = p; }
   bAA(_False p) { value_ = p; }
    static bAA True(){ return bAA{  _True{  }   };    };
    static bAA False(){ return bAA{  _False{  }   };    }; 
    bool is_True() const { return std::holds_alternative<_True>(value_); }
    bool is_False() const { return std::holds_alternative<_False>(value_); } 
    const _True&  as_True() const { return std::get<_True>(value_); }
    const _False&  as_False() const { return std::get<_False>(value_); } 
};



class bool {
    struct _True {};
    struct _False {};
    std::variant< _True, _False > value_;
public:
    bool() = default; 
    bool(_True p) { value_ = p; }
   bool(_False p) { value_ = p; }
    static bool True(){ return bool{  _True{  }   };    };
    static bool False(){ return bool{  _False{  }   };    }; 
    bool is_True() const { return std::holds_alternative<_True>(value_); }
    bool is_False() const { return std::holds_alternative<_False>(value_); } 
    const _True&  as_True() const { return std::get<_True>(value_); }
    const _False&  as_False() const { return std::get<_False>(value_); } 
};


template<typename T1 >
class tree {
    struct _Tip {};
    struct _Node {
      std::shared_ptr<tree>p1_;
      tree p1() const { return *p1_; }
      T1 p2_;
      const T1& p2() const { return p2_; }
      std::shared_ptr<tree>p3_;
      tree p3() const { return *p3_; }   
    };
    std::variant< _Tip, _Node > value_;
public:
    tree() = default; 
    tree(_Tip p) { value_ = p; }
   tree(_Node p) { value_ = p; }
    static tree Tip(){ return tree{  _Tip{  }   };    };
    static tree Node(tree p1, T1 p2, tree p3){ return tree{  _Node{ std::make_shared<tree>(p1), p2, std::make_shared<tree>(p3) }   };    }; 
    bool is_Tip() const { return std::holds_alternative<_Tip>(value_); }
    bool is_Node() const { return std::holds_alternative<_Node>(value_); } 
    const _Tip&  as_Tip() const { return std::get<_Tip>(value_); }
    const _Node&  as_Node() const { return std::get<_Node>(value_); } 
};


template<typename T1 >
class list {
    struct _Nil {};
    struct _Cons {
      T1 p1_;
      const T1& p1() const { return p1_; }
      std::shared_ptr<list>p2_;
      list p2() const { return *p2_; }   
    };
    std::variant< _Nil, _Cons > value_;
public:
    list() = default; 
    list(_Nil p) { value_ = p; }
   list(_Cons p) { value_ = p; }
    static list Nil(){ return list{  _Nil{  }   };    };
    static list Cons(T1 p1, list p2){ return list{  _Cons{ p1, std::make_shared<list>(p2) }   };    }; 
    bool is_Nil() const { return std::holds_alternative<_Nil>(value_); }
    bool is_Cons() const { return std::holds_alternative<_Cons>(value_); } 
    const _Nil&  as_Nil() const { return std::get<_Nil>(value_); }
    const _Cons&  as_Cons() const { return std::get<_Cons>(value_); } 
};



class nat {
    struct _Zero {};
    struct _Suc {
      std::shared_ptr<nat>p1_;
      nat p1() const { return *p1_; }   
    };
    std::variant< _Zero, _Suc > value_;
public:
    nat() = default; 
    nat(_Zero p) { value_ = p; }
   nat(_Suc p) { value_ = p; }
    static nat Zero(){ return nat{  _Zero{  }   };    };
    static nat Suc(nat p1){ return nat{  _Suc{ std::make_shared<nat>(p1) }   };    }; 
    bool is_Zero() const { return std::holds_alternative<_Zero>(value_); }
    bool is_Suc() const { return std::holds_alternative<_Suc>(value_); } 
    const _Zero&  as_Zero() const { return std::get<_Zero>(value_); }
    const _Suc&  as_Suc() const { return std::get<_Suc>(value_); } 
};



class sig {
    struct _cc {};
    std::variant< _cc > value_;
public:
    sig() = default; 
    sig(_cc p) { value_ = p; }
    static sig cc(){ return sig{  _cc{  }   };    }; 
    bool is_cc() const { return std::holds_alternative<_cc>(value_); } 
    const _cc&  as_cc() const { return std::get<_cc>(value_); } 
};


