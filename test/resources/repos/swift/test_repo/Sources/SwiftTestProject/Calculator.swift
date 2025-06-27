import Foundation

/// A simple calculator class for basic arithmetic operations
public class Calculator {
    
    public init() {}
    
    /// Adds two numbers
    /// - Parameters:
    ///   - a: First number
    ///   - b: Second number
    /// - Returns: Sum of a and b
    public func add(_ a: Int, _ b: Int) -> Int {
        return a + b
    }
    
    /// Subtracts second number from first
    /// - Parameters:
    ///   - a: First number
    ///   - b: Second number
    /// - Returns: Difference of a and b
    public func subtract(_ a: Int, _ b: Int) -> Int {
        return a - b
    }
    
    /// Multiplies two numbers
    /// - Parameters:
    ///   - a: First number
    ///   - b: Second number
    /// - Returns: Product of a and b
    public func multiply(_ a: Int, _ b: Int) -> Int {
        return a * b
    }
    
    /// Divides first number by second
    /// - Parameters:
    ///   - a: Dividend
    ///   - b: Divisor
    /// - Returns: Result of division
    /// - Throws: `CalculatorError.divisionByZero` if b is zero
    public func divide(_ a: Int, _ b: Int) throws -> Double {
        guard b != 0 else {
            throw CalculatorError.divisionByZero
        }
        return Double(a) / Double(b)
    }
    
    /// Calculates factorial of a number
    /// - Parameter n: Non-negative integer
    /// - Returns: Factorial of n
    /// - Throws: `CalculatorError.invalidInput` if n is negative
    public func factorial(_ n: Int) throws -> Int {
        guard n >= 0 else {
            throw CalculatorError.invalidInput("Factorial is not defined for negative numbers")
        }
        
        if n <= 1 {
            return 1
        }
        
        return n * try factorial(n - 1)
    }
}

/// Errors that can be thrown by Calculator
public enum CalculatorError: Error, LocalizedError {
    case divisionByZero
    case invalidInput(String)
    
    public var errorDescription: String? {
        switch self {
        case .divisionByZero:
            return "Cannot divide by zero"
        case .invalidInput(let message):
            return "Invalid input: \(message)"
        }
    }
}