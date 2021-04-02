from model.expense import Expense


class GroupTotalExpenseCalculator:
    @staticmethod
    def calc(group_id):
        query = Expense.query.filter(group_id == group_id)
        return sum(expense.price for expense in query.all())
