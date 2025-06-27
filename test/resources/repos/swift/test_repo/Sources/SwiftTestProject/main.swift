import Foundation

/// Entry point for the SwiftTestProject executable
@main
struct SwiftTestProject {
    static func main() {
        print("🚀 Welcome to SwiftTestProject!")
        
        // Test Calculator functionality
        let calculator = Calculator()
        let result = calculator.add(5, 3)
        print("Calculator: 5 + 3 = \(result)")
        
        // Test Person functionality
        let person = Person(name: "Alice", age: 30)
        print("Person: \(person.description)")
        
        // Test extensions
        let message = "hello world"
        print("Capitalized: \(message.capitalizeFirstLetter())")
        
        // Test async functionality
        Task {
            await demonstrateAsyncFunction()
        }
    }
    
    static func demonstrateAsyncFunction() async {
        print("Starting async operation...")
        try? await Task.sleep(nanoseconds: 1_000_000_000) // 1 second
        print("Async operation completed!")
    }
}