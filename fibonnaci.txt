program FibonacciSimple;

var
  n, i: integer;
  a, b, c: integer;

begin
  writeln('Entrez le nombre de termes : ');
  readln(n);

  a := 0;
  b := 1;

  writeln('Suite de Fibonacci : ');
  writeln(a);
  writeln(b);

  for i := 3 to n do
  begin
    c := a + b;
    writeln(c);
    a := b;
    b := c;
  end;
end.
