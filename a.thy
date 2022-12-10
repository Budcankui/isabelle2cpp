theory test
 imports Main
begin
datatype bAA=True|False
datatype bool=True|False
datatype 'a   tree=Tip|Node  "'a tree" 'a "'a tree"
datatype 'a list=Nil|Cons  'a  "'a list"
datatype nat= Zero | Suc nat
datatype  sig = cc
fun add :: "nat ⇒ nat ⇒ nat" where
"add Zero n=n"|
"add (Suc m) n=Suc(add m n)"

fun conj:: "bool ⇒ bool ⇒ bool" where
"conj True True = True"|
"conj _ _= False"

end