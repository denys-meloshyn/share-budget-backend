//
//  BudgetDetailPresenter.swift
//  ShareBudget
//
//  Created by Denys Meloshyn on 03.02.17.
//  Copyright © 2017 Denys Meloshyn. All rights reserved.
//

import CorePlot

protocol BudgetDetailPresenterDelegate: class {
    func updateBalance(_ balance: String)
    func updateMonthLimit(_ limit: String)
    func updateTotalExpense(_ total: String)
}

class BudgetDetailPresenter: BasePresenter {
    weak var delegate: BudgetDetailPresenterDelegate?
    
    fileprivate var budgetDetailInteraction: BudgetDetailInteraction {
        get {
            return self.interaction as! BudgetDetailInteraction
        }
    }
    
    private var budgetDetailRouter: BudgetDetailRouter {
        get {
            return self.router as! BudgetDetailRouter
        }
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        self.configureTotalExpenses()
        self.configureMonthBudget()
        self.configureBalance()
    }
    
    private func configureTotalExpenses() {
        let total = self.budgetDetailInteraction.totalExpenses()
        self.delegate?.updateTotalExpense(String(total))
    }
    
    private func configureMonthBudget() {
        let month = self.budgetDetailInteraction.lastMonthLimit()
        self.delegate?.updateMonthLimit(String(month?.limit ?? 0.0))
    }
    
    private func configureBalance() {
        self.delegate?.updateBalance(String(self.budgetDetailInteraction.balance()))
    }
    
    func createNewExpense() {
        self.budgetDetailRouter.openEditExpensePage(with: self.budgetDetailInteraction.budgetID)
    }
    
    func showAllExpenses() {
        self.budgetDetailRouter.showAllExpensesPage(with: self.budgetDetailInteraction.budgetID)
    }
}

// MARK: - CPTPieChartDataSource

extension BudgetDetailPresenter: CPTPieChartDataSource {
    func numberOfRecords(for plot: CPTPlot) -> UInt
    {
        return UInt(self.budgetDetailInteraction.numberOfExpenses())
    }
    
    func number(for plot: CPTPlot, field: UInt, record: UInt) -> Any?
    {
        let expense = self.budgetDetailInteraction.expense(for: Int(record))
        
        return expense.price as NSNumber
        //        if Int(record) > 10 {
        //            return nil
        //        }
        //        else {
        //            switch CPTPieChartField(rawValue: Int(field))! {
        //            case .sliceWidth:
        //                return NSNumber(value: record)
        //
        //            default:
        //                return record as NSNumber
        //            }
        //        }
    }
    
    func dataLabel(for plot: CPTPlot, record: UInt) -> CPTLayer?
    {
        let label = CPTTextLayer(text:"\(record)")
        
        if let textStyle = label.textStyle?.mutableCopy() as? CPTMutableTextStyle {
            textStyle.color = .lightGray()
            
            label.textStyle = textStyle
        }
        
        return label
    }
    
    //    func radialOffset(for piePlot: CPTPieChart, record recordIndex: UInt) -> CGFloat
    //    {
    //        var offset: CGFloat = 0.0
    //
    //        if ( recordIndex == 0 ) {
    //            offset = piePlot.pieRadius / 8.0
    //        }
    //
    //        return offset
    //    }
}

// MARK: - CPTPieChartDelegate

extension BudgetDetailPresenter: CPTPieChartDelegate {
    func pieChart(_ plot: CPTPieChart, sliceTouchDownAtRecord idx: UInt) {
        
    }
}
