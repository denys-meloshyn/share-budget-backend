//
//  CategoryPresenterTest.swift
//  ShareBudget
//
//  Created by Denys Meloshyn on 28.08.17.
//  Copyright © 2017 Denys Meloshyn. All rights reserved.
//

import XCTest
import CoreData
import Nimble
@testable import ShareBudget

class CategoryPresenterTest: XCTestCase {
    var view: CategoryView!
    var router: CategoryRouter!
    var presenter: CategoryPresenter!
    var interaction: CategoryInteraction!
    var viewController: MockCategoryViewController!
    
    var budget: Budget!
    var expense: Expense!
    var managedObjectContext: NSManagedObjectContext!
    
    override func setUp() {
        super.setUp()
        
        self.managedObjectContext = ModelManager.childrenManagedObjectContext(from: ModelManager.managedObjectContext)
        
        self.budget = Budget(context: self.managedObjectContext)
        self.budget.name = "Test budget"
        self.expense = Expense(context: self.managedObjectContext)
        self.budget.addToExpenses(expense)
        
        self.viewController = MockCategoryViewController()
        self.viewController.expenseID = self.expense.objectID
        self.viewController.managedObjectContext = self.managedObjectContext
        self.router = CategoryRouter(with: self.viewController)
        self.interaction = CategoryInteraction(with: self.expense.objectID, managedObjectContext: self.managedObjectContext)
        self.presenter = CategoryPresenter(with: self.interaction, router: self.router, delegate: nil)
        self.view = CategoryView(with: self.presenter, and: self.viewController)
        
        viewController.viperView = self.view
        
        self.viewController.tableView = UITableView()
        self.viewController.viewDidLoad()
    }
    
    override func tearDown() {
        ModelManager.dropAllEntities()
        
        super.tearDown()
    }
    
    private func addDefaultItems(number: Int = 1) {
        for i in 0..<number {
            let model = Category(context: self.managedObjectContext)
            model.name = "Name_\(i)"
            model.budget = self.budget
            self.budget.addToCategories(model)
        }
        
        ModelManager.saveContext(self.managedObjectContext)
    }
    
    // MARK: - Test
    
    func testHeaderModeCreate() {
        let result = BudgetHeaderMode.create
        let expected = self.presenter.headerMode()
        XCTAssertEqual(result, expected)
    }
    
    func testHeaderModeSearch() {
        self.addDefaultItems(number: 2)
        
        let result = BudgetHeaderMode.search
        let expected = self.presenter.headerMode()
        XCTAssertEqual(result, expected)
    }
    
    func testNumberOfRowsInSectionInTableView() {
        self.addDefaultItems(number: 10)
        
        let result = self.presenter.tableView(self.view.tableView!, numberOfRowsInSection: 0)
        expect(result) == 10
    }
    
    func testViewForHeaderInSectionNotEmpty() {
        self.addDefaultItems()
        
        let header = self.presenter.tableView(self.view.tableView!, viewForHeaderInSection: 0) as! CreateSearchTableViewHeader
        
        expect(header.textField?.text).notTo(beNil())
        expect(header.textField?.placeholder).notTo(beNil())
    }
}