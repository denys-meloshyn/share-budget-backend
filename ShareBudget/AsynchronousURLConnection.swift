//
//  AsynchronousURLConnection.swift
//  ShareBudget
//
//  Created by Denys Meloshyn on 13.01.17.
//  Copyright © 2017 Denys Meloshyn. All rights reserved.
//

import UIKit

class AsynchronousURLConnection: NSObject {
    typealias APICompletionBlock = (Any?, URLResponse?, Error?) -> (Void)
    
    static func runAsynchronousRequest(_ request: URLRequest, completion: APICompletionBlock?) -> URLSessionDataTask? {
        let task = AsynchronousURLConnection.createAsynchronousRequest(request, completion: completion)
        task?.resume()
        
        return task
    }
    
    static func createAsynchronousRequest(_ request: URLRequest, completion: APICompletionBlock?) -> URLSessionDataTask? {
        let sessionConfig = URLSessionConfiguration.default
        let session = URLSession(configuration: sessionConfig)
        
        let complitionResponseBlock = { (data: Data?, response: URLResponse?, error: Error?) -> Void in
            if let _ = error {
                completion?(data, response, error)
                return
            }
            
            if let httpResponse = response as? HTTPURLResponse, httpResponse.statusCode != 200 {
                completion?(data, response, error)
                return
            }
            
            guard let data = data else {
                completion?(nil, response, error)
                return
            }
            
            do {
                let result = try JSONSerialization.jsonObject(with: data, options: JSONSerialization.ReadingOptions.mutableContainers)
                completion?(result, response, error)
            }
            catch {
                completion?(data, response, error)
            }

        }
        
        let task = session.dataTask(with: request, completionHandler: complitionResponseBlock)
        
        return task
    }
}
