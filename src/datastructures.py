
"""
update this file to implement the following already declared methods:
- add_member: Should add a member to the self._members list
- delete_member: Should delete a member from the self._members list
- update_member: Should update a member from the self._members list
- get_member: Should return a member from the self._members list
"""

class FamilyStructure:
    def __init__(self, last_name):
        self.last_name = last_name
        self._next_id = 1
        # example list of members
        self._members = []
        self._default_members = [
            {
                "first_name": "John",
                "age": 33,
                "lucky_numbers": {7, 13, 22},
                "id": self._generate_id(),
            },
            {
                "first_name": "Jane",
                "age": 35,
                "lucky_numbers": {10, 14, 3},
                "id": self._generate_id(),
            },
            {
                "first_name": "Jimmy",
                "age": 5,
                "lucky_numbers": {1},
                "id": self._generate_id(),
            }
        ]
        for member in self._default_members:
            self._members.append(member)

    # read-only: Use this method to generate random members ID's when adding members into the list
    def _generate_id(self):
        generated_id = self._next_id
        self._next_id += 1
        return generated_id

    def add_member(self, member):
        # fill this method and update the return
        #Comprueba que member sea un diccionario
        if not isinstance(member, dict):
            raise TypeError("The member must be a dict")
        #Comprueba que member el lucky_number sea un conjunto(set), si no lo es, lo transforma
        if 'lucky_numbers' in member and not isinstance(member['lucky_numbers'], set):
            member['lucky_numbers'] = set(member['lucky_numbers'])
        #Comprueba si 'age' sea un int mayor que 0
        if not isinstance(member['age'], int) or member['age'] <= 0:
            raise ValueError("Age must be a positive integer")
        #Comprueba que exista id en member
        if 'id' not in member:
            member['id'] = self._generate_id()
        #Fuerza el apellido de la clase
        member['last_name'] = self.last_name
        self._members.append(member)
        return member
        

    def delete_member(self, id):
        # fill this method and update the return
        #Verifica la longitud del array
        initial_len = len(self._members)
        #Recorre los miembros devolviendo sólo aquellos donde el 'id' es diferente al 'id' dado como argumento
        self._members = [memb for memb in self._members if memb['id'] != id]
        #Utilizo operador de comparación para retornar un booleano. True si la función se cumple.
        return len(self._members) < initial_len


    def get_member(self, id):
        #Recorre los miembros dentro de self._members, retornando el miembro con el 'id' dado como argumento.
        for member in self._members:
            if member['id'] == id:
                return member
        #Si no encuentra al miembro con el 'id' dado retorna None
        return None

    # this method is done, it returns a list with all the family members
    def get_all_members(self):
        return self._members

