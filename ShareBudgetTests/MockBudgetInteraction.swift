//
//  MockBudgetInteraction.swift
//  ShareBudget
//
//  Created by Denys Meloshyn on 18.05.17.
//  Copyright © 2017 Denys Meloshyn. All rights reserved.
//

import UIKit
import CoreData
@testable import ShareBudget

class MockBudgetInteraction: BudgetInteraction {
    var numberOfItems = 0
    
    override func numberOfRowsInSection() -> Int {
        return numberOfItems
    }
    
    override func budgetModel(for indexPath: IndexPath) -> Budget {
        let model = Budget(context: ModelManager.managedObjectContext)
        model.name = "Test name"
        
        return model
    }
}
