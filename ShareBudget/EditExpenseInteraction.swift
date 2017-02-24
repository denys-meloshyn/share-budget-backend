//
//  EditExpenseInteraction.swift
//  ShareBudget
//
//  Created by Denys Meloshyn on 05.02.17.
//  Copyright © 2017 Denys Meloshyn. All rights reserved.
//

import CoreData

class EditExpenseInteraction: BaseInteraction {
    var budget: Budget
    var expense: Expense
    let managedObjectContext = ModelManager.childrenManagedObjectContext(from: ModelManager.managedObjectContext)
    
    private var expenseID: NSManagedObjectID?
    
    init(with budgetID: NSManagedObjectID, expenseID: NSManagedObjectID?) {
        self.expenseID = expenseID
        self.budget = self.managedObjectContext.object(with: budgetID) as! Budget
        
        if let expenseID = expenseID {
            self.expense = self.managedObjectContext.object(with: expenseID) as! Expense
        }
        else {
            self.expense = Expense(context: self.managedObjectContext)
            self.expense.creationDate = NSDate()
            self.expense.budget = self.budget
            self.budget.addToExpenses(self.expense)
        }
    }
    
    var isExpenseNew: Bool {
        if self.expenseID == nil {
            return true
        }
        
        return false
    }
    
    func save() {
        self.expense.isChanged = true
        ModelManager.saveChildren(self.managedObjectContext)
    }
    
    func updateCategory(_ categoryID: NSManagedObjectID) {
        self.expense.category = self.managedObjectContext.object(with: categoryID) as? Category
    }
}
