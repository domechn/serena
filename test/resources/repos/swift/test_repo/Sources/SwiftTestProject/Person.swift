import Foundation

/// Represents a person with basic information
public struct Person {
    public let name: String
    public let age: Int
    public let email: String?
    
    /// Creates a new Person instance
    /// - Parameters:
    ///   - name: Person's name
    ///   - age: Person's age
    ///   - email: Optional email address
    public init(name: String, age: Int, email: String? = nil) {
        self.name = name
        self.age = age
        self.email = email
    }
    
    /// Computed property to check if person is an adult
    public var isAdult: Bool {
        return age >= 18
    }
    
    /// Returns a greeting message
    /// - Parameter timeOfDay: Optional time of day for personalized greeting
    /// - Returns: Personalized greeting string
    public func greet(timeOfDay: TimeOfDay = .any) -> String {
        let greeting = timeOfDay.greeting
        return "\(greeting), my name is \(name)!"
    }
    
    /// Updates email address
    /// - Parameter newEmail: New email address
    /// - Returns: New Person instance with updated email
    public func withEmail(_ newEmail: String) -> Person {
        return Person(name: name, age: age, email: newEmail)
    }
}

// MARK: - CustomStringConvertible
extension Person: CustomStringConvertible {
    public var description: String {
        let emailInfo = email.map { " (\($0))" } ?? ""
        return "\(name), \(age) years old\(emailInfo)"
    }
}

// MARK: - Equatable
extension Person: Equatable {
    public static func == (lhs: Person, rhs: Person) -> Bool {
        return lhs.name == rhs.name && 
               lhs.age == rhs.age && 
               lhs.email == rhs.email
    }
}

// MARK: - Codable
extension Person: Codable {}

/// Time of day enumeration for greetings
public enum TimeOfDay: String, CaseIterable {
    case morning = "morning"
    case afternoon = "afternoon"
    case evening = "evening"
    case any = "any"
    
    var greeting: String {
        switch self {
        case .morning:
            return "Good morning"
        case .afternoon:
            return "Good afternoon"
        case .evening:
            return "Good evening"
        case .any:
            return "Hello"
        }
    }
}