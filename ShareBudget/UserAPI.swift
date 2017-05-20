//
//  UserAPI.swift
//  ShareBudget
//
//  Created by Denys Meloshyn on 13.01.17.
//  Copyright © 2017 Denys Meloshyn. All rights reserved.
//

import CoreData

class UserAPI: BaseAPI {
    override func timestampStorageKey() -> String {
        return "user_timestamp"
    }
    
    override func parseUpdates(items: [[String: AnyObject?]], in managedObjectContext: NSManagedObjectContext) {
        var user: User?
        
        for item in items {
            user = User(context: managedObjectContext)
            user?.update(with: item, in: managedObjectContext)
        }
    }
}
