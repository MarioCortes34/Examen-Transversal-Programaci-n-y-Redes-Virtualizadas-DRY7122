a = int(input("ingrese el numero de Vlan para consultar: "))

if a >= 1 and a <= 1005 :
        print(f"La VLAN {a} pertenece al Rango Normal.")
elif a >= 1006 and a <= 4094:
        print(f"La VLAN {a} pertenece al Rango Extendido.")
else:
        print(f"La VLAN {a} es Incorecta fuera del Rango.")