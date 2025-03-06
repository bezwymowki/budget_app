class Category:

    def __init__(self, name):
        self.name = name
        self.ledger = []

    def __str__(self):
        category_list = []
        title = f"{self.name:^30}"
        category_list.append(title.replace(" ", "*"))
        for item in self.ledger:
            description = item["description"][:23]
            amount = f"{item['amount']:7.2f}"
            category_list.append(f"{description:23}{amount:>7}")
        category_list.append(f"Total: {self.get_balance()}")
        return "\n".join(category_list)



    def deposit(self, amount, description = None):
        if description is None:
            description = ""
        deposit = {'amount': amount, 'description': description}
        self.ledger.append(deposit)
        

    def withdraw(self, amount, description = None):
        if description is None:
            description = ""
        
        if self.check_funds(amount):
            withdraw = {'amount': -amount, 'description': description}
            self.ledger.append(withdraw)
            return True
        else:
            return False    


    def get_balance(self):
        current_balance = 0
        for entry in self.ledger:
            current_balance += entry['amount']
        
        return current_balance


    def transfer(self, amount, budget_category):
        if self.check_funds(amount):
            self.withdraw(amount, f"Transfer to {budget_category.name}")
            budget_category.deposit(amount, f"Transfer from {self.name}")
            return True
        return False
        

    def check_funds(self, amount):
        return amount <= self.get_balance()




def create_spend_chart(categories):
    withdraw_sum = []
    deposit_sum = []
    for category in categories:
        withdraw_sum.append(-sum(item["amount"] for item in category.ledger if item["amount"] < 0))
        deposit_sum.append(sum(item["amount"] for item in category.ledger if item["amount"] > 0))
        
    percentages = []
    for i, category in enumerate(categories):
        percentage = (withdraw_sum[i] / deposit_sum[i]) * 100
        percentages.append((category.name, int(percentage // 10) * 10))

    print("Percentage spent by category")

    max_height = 10
    for row in range(max_height, 0, -1):
        line = ""
        for category, percentage in percentages:
            if percentage >= row * 10:
                line +="o "
            else:
                line += "  "
        print(f"{row * 10:3}| {line}")
    print(f"    {len(categories) * '---'}")

    max_name_length = max([len(category.name) for category in categories])
    for i in range(max_name_length):
        line = "    "
        for category, _ in percentages:
            if i < len(category):
                line += f" {category[i]} "
            else:
                line += f" {' '} "
        print(line)

#
food = Category("food")
clothes = Category("clothes")
food.deposit(1000)
food.withdraw(10, "cake")
food.transfer(500, clothes)
clothes.withdraw(200, "jeans")

category_list = [food, clothes]

create_spend_chart(category_list)