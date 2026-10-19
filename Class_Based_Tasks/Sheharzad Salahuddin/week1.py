"""Week 1 - Class Based Tasks."""

def find_max_min(nums):
    """Return (maximum, minimum) of nums without using built-in max/min."""
    if not nums:
        raise ValueError("nums must not be empty")
    maximum = minimum = nums[0]
    for n in nums[1:]:
        if n > maximum:
            maximum = n
        elif n < minimum:
            minimum = n
    return maximum, minimum


BELOW_20 = [
    "", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine",
    "Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen",
    "Seventeen", "Eighteen", "Nineteen",
]
TENS = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]
SCALES = ["", "Thousand", "Million", "Billion", "Trillion"]


def _three_digits(n):
    """Convert 0 <= n < 1000 to words (empty string for 0)."""
    words = []
    if n >= 100:
        words += [BELOW_20[n // 100], "Hundred"]
        n %= 100
    if n >= 20:
        words.append(TENS[n // 10])
        n %= 10
    if n > 0:
        words.append(BELOW_20[n])
    return " ".join(words)


def number_to_words(num):
    if num < 0:
        raise ValueError("num must be non-negative")
    if num == 0:
        return "Zero"
    parts = []
    scale = 0
    while num > 0:
        chunk = num % 1000
        if chunk:
            part = _three_digits(chunk)
            if SCALES[scale]:
                part += " " + SCALES[scale]
            parts.append(part)
        num //= 1000
        scale += 1
    return " ".join(reversed(parts))

class Product:
    def __init__(self, product_id, name, price, stock):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock = stock

    def __repr__(self):
        return f"{self.product_id:<6}{self.name:<20}{self.price:>10.2f}{self.stock:>8}"


class Inventory:
    def __init__(self):
        self.products = {}

    def add_product(self, product_id, name, price, stock):
        if product_id in self.products:
            raise ValueError(f"Product '{product_id}' already exists")
        self.products[product_id] = Product(product_id, name, price, stock)

    def update_product(self, product_id, price=None, stock=None):
        product = self.get(product_id)
        if price is not None:
            product.price = price
        if stock is not None:
            product.stock = stock

    def remove_product(self, product_id):
        self.get(product_id)
        del self.products[product_id]

    def get(self, product_id):
        if product_id not in self.products:
            raise KeyError(f"Product '{product_id}' not found")
        return self.products[product_id]

    def show(self):
        print(f"{'ID':<6}{'Name':<20}{'Price':>10}{'Stock':>8}")
        print("-" * 44)
        for product in self.products.values():
            print(product)


class Bill:
    TAX_RATE = 0.17

    def __init__(self, inventory, customer_name, discount_percent=0):
        self.inventory = inventory
        self.customer_name = customer_name
        self.discount_percent = discount_percent
        self.items = {}  # product_id -> quantity

    def add_item(self, product_id, quantity):
        product = self.inventory.get(product_id)
        already = self.items.get(product_id, 0)
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        if already + quantity > product.stock:
            raise ValueError(f"Only {product.stock} of '{product.name}' in stock")
        self.items[product_id] = already + quantity

    def remove_item(self, product_id):
        self.items.pop(product_id, None)

    def subtotal(self):
        return sum(self.inventory.get(pid).price * qty for pid, qty in self.items.items())

    def discount(self):
        return self.subtotal() * self.discount_percent / 100

    def tax(self):
        return (self.subtotal() - self.discount()) * self.TAX_RATE

    def total(self):
        return self.subtotal() - self.discount() + self.tax()

    def checkout(self):
        """Deduct purchased quantities from stock and return the invoice text."""
        for pid, qty in self.items.items():
            self.inventory.get(pid).stock -= qty
        return self.invoice()

    def invoice(self):
        lines = [
            "=" * 50,
            "INVOICE".center(50),
            f"Customer: {self.customer_name}",
            "=" * 50,
            f"{'Item':<20}{'Qty':>6}{'Price':>12}{'Amount':>12}",
            "-" * 50,
        ]
        for pid, qty in self.items.items():
            p = self.inventory.get(pid)
            lines.append(f"{p.name:<20}{qty:>6}{p.price:>12.2f}{p.price * qty:>12.2f}")
        lines += [
            "-" * 50,
            f"{'Subtotal:':<38}{self.subtotal():>12.2f}",
            f"{f'Discount ({self.discount_percent}%):':<38}{-self.discount():>12.2f}",
            f"{f'Tax ({self.TAX_RATE * 100:.0f}%):':<38}{self.tax():>12.2f}",
            f"{'TOTAL:':<38}{self.total():>12.2f}",
            "=" * 50,
        ]
        return "\n".join(lines)

def fizz_buzz(n):
    answer = []
    for i in range(1, n + 1):
        if i % 15 == 0:
            answer.append("FizzBuzz")
        elif i % 3 == 0:
            answer.append("Fizz")
        elif i % 5 == 0:
            answer.append("Buzz")
        else:
            answer.append(str(i))
    return answer

def two_sum(nums, target):
    """Return indices [i, j] such that nums[i] + nums[j] == target. O(n)."""
    seen = {}  # value -> index
    for i, n in enumerate(nums):
        complement = target - n
        if complement in seen:
            return [seen[complement], i]
        seen[n] = i
    return []

if __name__ == "__main__":
    print("Task 1:", find_max_min([3, 7, -2, 15, 0, 9]))

    print("\nTask 2:")
    for num in (0, 13, 123, 12345, 1234567, 1000010):
        print(f"  {num} -> {number_to_words(num)}")

    print("\nTask 3:")
    inventory = Inventory()
    inventory.add_product("P1", "Notebook", 120.0, 50)
    inventory.add_product("P2", "Pen", 25.0, 200)
    inventory.add_product("P3", "Backpack", 1500.0, 10)
    inventory.show()
    bill = Bill(inventory, "Ali Khan", discount_percent=10)
    bill.add_item("P1", 3)
    bill.add_item("P2", 10)
    bill.add_item("P3", 1)
    print(bill.checkout())
    print("\nStock after checkout:")
    inventory.show()

    print("\nTask 4:", fizz_buzz(15))

    print("\nTask 5:", two_sum([2, 7, 11, 15], 9), two_sum([3, 2, 4], 6))
