//
//  URLRequest+UserCredentials.swift
//  ShareBudget
//
//  Created by Denys Meloshyn on 22.01.17.
//  Copyright © 2017 Denys Meloshyn. All rights reserved.
//

import UIKit

extension URLRequest {
    mutating func addToken() {
        self.setValue(UserCredentials.token, forHTTPHeaderField: kToken)
    }
    
    mutating func addUpdateCredentials(timestamp: String) {
        self.addToken()
        self.setValue(String(UserCredentials.userID), forHTTPHeaderField: kUserID)
        
        if timestamp.characters.count > 0 {
            self.setValue(timestamp, forHTTPHeaderField: kTimeStamp)
        }
    }
}