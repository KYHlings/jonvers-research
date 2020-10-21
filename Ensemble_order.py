from random import shuffle


class Developer:
    def __init__(self, name, role):
        self.name = name
        if role:
            self.role = "Driver"
        else:
            self.role = "Navigator"

    def change_role(self):
        if self.role == "Driver":
            self.role = "Navigator"
        else:
            self.role = "Driver"


def main():
    developer_names = ["Elizabeth", "David", "Daniel", "Jonathan", "Tobias"]
    shuffle(developer_names)
    developer_ls = [Developer(developer_names[i], i % 2 == 0) for i in range(len(developer_names))]
    j = 0
    for i in range(len(developer_ls)):
        print(f"Driver: {developer_ls[i].name}")
        developer_ls[j].change_role()
        if j == len(developer_ls)-1:
            j = 0
        else:
            j += 1


if __name__ == '__main__':
    main()
