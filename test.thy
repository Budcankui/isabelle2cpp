theory test
  imports Main
begin 

(*bool*)
datatype sbool=True|False

fun conj:: "sbool \<Rightarrow> sbool \<Rightarrow> sbool" where
"conj True True = True"|
"conj True False= False"|
"conj False True= False"|
"conj False False= False"

(*snat*)
datatype snat=Zero|Suc snat

fun add:: "snat \<Rightarrow>snat \<Rightarrow> snat"where
"add Zero n=n"|
"add (Suc m) n=Suc(add m n)"

fun  min:: "snat \<Rightarrow>snat \<Rightarrow> snat"where
"min a Zero= a"|
"min Zero b= Zero"|
"min (Suc a) (Suc b)=min a b "

value " min (Suc (Suc Zero)) (Suc Zero) "

(*slist*)
datatype 'a slist=Nil|Cons 'a "'a slist"

(*# cons *)
fun cons::"'a \<Rightarrow>'a slist\<Rightarrow>'a slist" where
"cons  x Nil= (Cons x Nil)"|
"cons  x xs=(Cons x xs)"
(*  ! ! !Cons cons is diff! ! !*)
value " cons (Suc Zero)  Nil "
value " Cons (Suc Zero)  Nil "
(* slist *)
(* addHead *)
fun addListHead::"'a\<Rightarrow>'a slist\<Rightarrow>'a slist" where
"addListHead a Nil= Cons a Nil"|
"addListHead a xs=Cons a xs"
value "(addListHead (1::nat) (cons 0 (cons 0 Nil)))"
value "(addListHead (Suc Zero) (cons Zero (cons Zero Nil)))"


(* addTail  *)
fun addListTail::"'a\<Rightarrow>'a slist\<Rightarrow>'a slist" where
"addListTail a Nil= cons a Nil"|
"addListTail a (Cons x xs) =(Cons  x  (addListTail a xs))"
value "(addListTail (1::nat) (cons 0 (cons 0 Nil)))"

(* addListI  *)
fun addListI::"'a\<Rightarrow>snat\<Rightarrow>'a slist\<Rightarrow>'a slist" where
"addListI a n Nil = Cons a Nil"|
"addListI a Zero xs =Cons a xs"|
"addListI a (Suc n) (Cons x xs) =Cons x  (addListI a n xs)"
value "addListI (100::nat) (Suc Zero)  (cons 1 (cons 2 Nil))"

(* delListHead  *)
fun delListHead::"'a slist\<Rightarrow>'a slist" where
"delListHead  Nil = Nil"|
"delListHead (Cons x xs) = xs"
value "delListHead  (cons (1::nat) (cons 2 Nil))"

(* delListTail  *)
fun delListTail::"'a slist\<Rightarrow>'a slist" where
"delListTail  Nil = Nil"|
"delListTail  (Cons x Nil) = Nil"|
"delListTail (Cons x xs) =( Cons x ( delListTail xs))"
value "delListTail  (cons (1::nat) (cons 2 Nil))"

(* delListI  *)
fun delListI::"snat\<Rightarrow>'a slist\<Rightarrow>'a slist" where
"delListI  n Nil = Nil"|
"delListI  Zero (Cons x xs) = xs"|
"delListI  (Suc n) (Cons x xs) =Cons  x  (delListI  n xs)"
value "delListI  (Suc Zero) (cons (1::nat) (cons 2 (cons 3 Nil)))"

(* searchList  *)
fun searchList::"'a\<Rightarrow>'a slist\<Rightarrow>sbool" where
"searchList  a  Nil = False"|
"searchList  a  (Cons x xs) = (if a=x then True else (searchList a xs))"
value "searchList  1   (cons (1::nat) (cons 2 (cons 3 Nil)))"
value "searchList  (Suc Zero)   (cons (Suc Zero) (cons (Suc (Suc Zero)) Nil) )"

fun replaceList::"'a\<Rightarrow>'a\<Rightarrow>'a slist\<Rightarrow>'a slist" where
"replaceList  a b Nil=Nil"|
"replaceList  a b (Cons x xs) = (if a=x then Cons b xs  else Cons x (replaceList a  b xs) )"
value "replaceList  2  10 (cons (1::nat) (cons 2 (cons 3 Nil))) "

fun replaceListI::"'a\<Rightarrow>snat\<Rightarrow>'a slist\<Rightarrow>'a slist" where
"replaceListI  a n Nil=Nil"|
"replaceListI  a  Zero (Cons x xs) = Cons a xs"|
"replaceListI  a (Suc n) (Cons x xs) = Cons x (replaceListI a n xs)"
value "replaceListI  10 (Suc Zero) (cons (1::nat) (cons 2 (cons 3 Nil)))"


fun filter1::"('a\<Rightarrow>bool)\<Rightarrow>'a slist\<Rightarrow>'a slist" where
"filter1 func Nil=Nil"|
"filter1 func (Cons x xs)=(if (func x) then Cons x (filter1 func xs)
                   else filter1 func xs )"

fun filter2::"('a\<Rightarrow>sbool)\<Rightarrow>'a slist\<Rightarrow>'a slist" where
"filter2 func Nil=Nil"|
"filter2 func (Cons x xs)=(if (func x)=True then Cons x (filter2 func xs)
                   else filter2 func xs )"
fun call_back_func::"nat \<Rightarrow> sbool" where
"call_back_func n  = (if n \<le> 2 then True else False)"

value "filter (\<lambda>y::nat. y\<le>2)  [1,2,3]"
value "filter1  (\<lambda>y::nat. y\<le>2)  (cons (1::nat) (cons 2 (cons 3 Nil)))"
value "filter2  call_back_func   (cons (1::nat) (cons 2 (cons 3 Nil)))"


(*append @ [xs] x \<Longrightarrow> [xs,x] *)
(*useful  *)
fun app::"'a slist\<Rightarrow>'a \<Rightarrow>'a slist" where
"app  Nil a= cons a Nil"|
"app (Cons x xs)  a= Cons x (app  xs a)"
value "app (cons (1::nat) (cons 2 (cons 3 Nil))) (10::nat)"

fun revList::"'a slist\<Rightarrow>'a slist" where
"revList Nil= Nil"|
"revList (Cons x xs)=app (revList xs) x"
value "revList (cons 1 (cons 2 (cons (3::nat) Nil)))"



fun insert::"'a::ord\<Rightarrow>'a slist\<Rightarrow>'a slist" where
"insert a Nil=cons a Nil"|
"insert a (Cons x xs)=(if a\<le>x then Cons a (Cons x xs)
                 else Cons x (insert a xs)  )"
value "insert (3::nat) (cons 1 (cons 2 (cons (4::nat) Nil)))"

fun insertSort::"('a::ord) slist\<Rightarrow>'a slist\<Rightarrow>'a slist "where
"insertSort Nil  ys =ys"|
"insertSort (Cons x xs) ys =insertSort xs (insert x ys)"
value "insertSort  (cons 4 (cons 2 (cons (6::nat) Nil))) (cons 1 (cons 3 (cons (5::nat) Nil)))"

fun merge::"'a::ord slist\<Rightarrow>'a slist\<Rightarrow>'a slist" where
"merge xs Nil=xs"|
"merge Nil ys=ys"|
"merge (Cons x xs) (Cons y ys)=(if x\<le>y then cons x (merge xs (Cons y ys))
                     else cons y (merge (Cons x xs) ys) )"

(*sb wan yi  ..... i am out  *)
fun mergeListSort::"('a::ord) slist\<Rightarrow>'a slist" where
"mergeListSort Nil=Nil"|
"mergeListSort (Cons x Nil)= (Cons x Nil)"|
"mergeListSort xs=merge (mergeListSort (take ((size xs) div 2) xs)) (mergeListSort (drop ((size xs) div 2) xs))"
value "mergeListSort [1::nat,10,6,17,9]"

fun quickSort::"('a::ord) list\<Rightarrow>'a list" where
"quickSort []=[]"|
"quickSort (x#xs)=
(quickSort(filter (\<lambda>y. y\<le>x) xs))@x#(quickSort(filter (\<lambda>y. y>x) xs))"
value "quickSort [1::nat,10,6,17,9]"



(*fun rightest::"'a tree \<Rightarrow> 'a" where
"rigthest (Node l x r) = (if r=Tip then x else rigthest r)"*)



(*tree*)
datatype 'a tree=Tip|Node  "'a tree" 'a "'a tree"

(*search*)
fun preSearchTree::"'a \<Rightarrow> 'a tree \<Rightarrow> bool" where
"preSearchTree a Tip = False"|
"preSearchTree a (Node left x right)= (if a = x then True
                                     else if (preSearchTree a left) then True
                                     else (preSearchTree a right))"
fun midSearchTree::"'a \<Rightarrow> 'a tree \<Rightarrow> bool" where
"midSearchTree a Tip = False"|
"midSearchTree a (Node left x right)= (if (midSearchTree a left) then True 
                                     else if a=x  then True
                                     else (midSearchTree a right))"
fun postSearchTree::"'a \<Rightarrow> 'a tree \<Rightarrow> bool" where
"postSearchTree a Tip = False"|
"postSearchTree a (Node left x right)= (if (postSearchTree a left) then True 
                                     else if (postSearchTree a right) then True
                                     else if a=x then True 
                                     else False)"
value "postSearchTree (2::nat) ( Node (Node Tip 1 Tip) 3 (Node Tip 2 Tip))"

(*insert *)
fun insTree::"'a::ord \<Rightarrow> 'a tree \<Rightarrow> 'a tree" where
"insTree a Tip = Node Tip a Tip"|
"insTree a (Node l x r) = (if a\<le>x then Node (insTree a l) x r 
else Node l x (insTree a r))"
value "insTree (1::nat) (Node Tip 2 Tip)"
value "insTree (9::nat) (Node (Node Tip 2 Tip) 4 (Node Tip 8 Tip))"

(* traverse *)
fun preTraverseTree::"'a tree \<Rightarrow> 'a list" where
"preTraverseTree Tip = []"|
"preTraverseTree (Node l x r) = x#(preTraverseTree l)@(preTraverseTree r)"
value "preTraverseTree  (Node (Node Tip 1 Tip) (2::nat) (Node Tip 3 Tip))"

fun midTraverseTree::"'a tree \<Rightarrow> 'a list" where
"midTraverseTree Tip = []"|
"midTraverseTree (Node l x r) = (midTraverseTree l)@x#(midTraverseTree r)"
value "midTraverseTree  (Node (Node Tip 1 Tip) (2::nat) (Node Tip 3 Tip))"

fun postTraverseTree::"'a tree \<Rightarrow> 'a list" where
"postTraverseTree Tip = []"|
"postTraverseTree (Node l x r) = app ((postTraverseTree l)@(postTraverseTree r)) x"
value "postTraverseTree  (Node (Node Tip 1 Tip) (2::nat) (Node Tip 3 Tip))"

(*delete*)
(*rightest*)
fun rightest::"'a tree \<Rightarrow> 'a" where
"rightest (Node l x r) = (if r = Tip then x else rightest r)"

(*rightestLeft*)
fun rightestLeft::"'a tree \<Rightarrow> 'a tree" where
"rightestLeft Tip = Tip"|
(*l x r if r then l ! ! ! *)
"rightestLeft (Node l x r) = (if r = Tip then l
                                     else (Node l x (rightestLeft r)))"
value "rightestLeft  (Node (Node Tip 1 Tip) (2::nat) (Node Tip 3 Tip))"

fun deleteRoot::"'a tree \<Rightarrow> 'a tree" where
"deleteRoot Tip = Tip"|
"deleteRoot (Node left x right) = (if right = Tip then left
                                   else if left = Tip then right
                                   else (Node (rightestLeft left) (rightest left) right))"
value "deleteRoot  (Node (Node Tip 1 Tip) (2::nat) (Node Tip 3 Tip))"

fun deleteTree::"'a::ord \<Rightarrow> 'a tree \<Rightarrow> 'a tree" where
"deleteTree a Tip = Tip"|
"deleteTree a (Node left x right) = (if a = x then (deleteRoot (Node left x right))
                                     else if a < x then (Node (deleteTree a left) x right)
                                     else (Node left x (deleteTree a right)))" 
value "deleteTree 1  (Node (Node Tip 1 Tip) (2::nat) (Node Tip 3 Tip))"

(* sort rep *)
fun replaceTree::"'a::ord \<Rightarrow> 'a::ord \<Rightarrow> 'a tree \<Rightarrow> 'a tree" where
"replaceTree a b Tip = Tip"|
"replaceTree a b (Node l x r) = (if midSearchTree a (Node l x r) = True
                                       then (insTree b (deleteTree a (Node l x r)))
                                       else (Node l x r))"
value "replaceTree 2 0  (Node (Node Tip 1 Tip) (2::nat) (Node Tip 3 Tip))"
(* nosort rep *)
fun replaceTree2::"'a::ord \<Rightarrow> 'a::ord \<Rightarrow> 'a tree \<Rightarrow> 'a tree" where
"replaceTree2 a b Tip = Tip"|
"replaceTree2 a b (Node l x r) = 
(if a=x then Node l b r 
  else if a<x  then Node (replaceTree2 a b l )  x r
  else Node l x (replaceTree2 a b r) 
)"
value "replaceTree2 1 10  (Node (Node Tip 1 Tip) (2::nat) (Node Tip 3 Tip))"

(*traverse to list then sort*)
fun listSortTree::"'a::ord tree \<Rightarrow> 'a list" where
"listSortTree a = quickSort  (preTraverseTree a)"
value "listSortTree  (Node (Node Tip 1 Tip) (2::nat) (Node Tip 3 Tip))"

(* sortTree then midTraverse*)
fun midTraverseSortTree::"'a tree \<Rightarrow> 'a list" where
"midTraverseSortTree a = midTraverseTree a"
value "midTraverseSortTree  (Node (Node Tip 1 Tip) (2::nat) (Node Tip 3 Tip))"


end