//
//  BarButtonItemListener.swift
//  ShareBudget
//
//  Created by Denys Meloshyn on 05.06.2018.
//  Copyright © 2018 Denys Meloshyn. All rights reserved.
//

import UIKit

typealias BarButtonItemListenerActionBlock = (BarButtonItemListener) -> Void

class BarButtonItemListener {
    var barButtonItem: UIBarButtonItem {
        return UIBarButtonItem(barButtonSystemItem: style, target: self, action: #selector(BarButtonItemListener.targetAction))
    }
    
    private let style: UIBarButtonSystemItem
    private let actionBlock: BarButtonItemListenerActionBlock?
    
    init(with style: UIBarButtonSystemItem, action: @escaping BarButtonItemListenerActionBlock) {
        self.style = style
        actionBlock = action
    }
    
    @objc func targetAction() {
        actionBlock?(self)
    }
}
