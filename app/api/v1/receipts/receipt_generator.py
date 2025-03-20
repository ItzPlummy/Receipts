from math import ceil, floor

from app.database.models import Receipt, Product


class ReceiptGenerator:
    fop_name: str = "ФОП Джонсонюк Борис"

    __receipt_width: int = 32

    @classmethod
    def generate(cls, receipt: Receipt) -> str:
        builder: str = cls.__center_string(cls.fop_name)

        builder += cls.__wide_line()

        for index, product in enumerate(receipt.products):
            builder += cls.__product(product)
            if index + 1 < len(receipt.products):
                builder += cls.__narrow_line()

        builder += cls.__wide_line()
        builder += cls.__side_strings("СУМА", f"{float(receipt.total):_.2f}")
        builder += cls.__side_strings("Картка", f"{float(receipt.payment_amount):_.2f}")
        builder += cls.__side_strings("Решта", f"{float(receipt.rest):_.2f}")

        builder += cls.__wide_line()
        builder += cls.__center_string(receipt.created_at.strftime("%Y.%m.%d %H:%M"))
        builder += cls.__center_string("Дякуємо за покупку!")

        builder.removesuffix("\n")

        return builder

    @classmethod
    def __product(cls, product: Product) -> str:
        builder: str = cls.__side_strings(f"{product.quantity} x {float(product.price):_.2f}")

        name: str = product.name
        lines: int = 0
        max_length: int = cls.__receipt_width - len(f"{float(product.total):_.2f}") - 1
        while name != "":
            if len(name) >= max_length:
                prefix: str = name[lines * max_length:(lines + 1) * max_length]
                builder += cls.__side_strings(prefix)
            else:
                prefix: str = name
                builder += cls.__side_strings(prefix, f"{float(product.total):_.2f}")

            name = name.removeprefix(prefix)

        return builder

    @classmethod
    def __center_string(cls, string: str) -> str:
        border_length: float = (cls.__receipt_width - len(string)) / 2

        return " " * ceil(border_length) + string + " " * floor(border_length) + "\n"

    @classmethod
    def __side_strings(cls, string_1: str = "", string_2: str = "") -> str:
        return string_1 + " " * (cls.__receipt_width - len(string_1) - len(string_2)) + string_2 + "\n"

    @classmethod
    def __narrow_line(cls) -> str:
        return "-" * cls.__receipt_width + "\n"

    @classmethod
    def __wide_line(cls) -> str:
        return "=" * cls.__receipt_width + "\n"
