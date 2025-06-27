import XCTest
@testable import SwiftTestProject

final class CalculatorTests: XCTestCase {
    
    var calculator: Calculator!
    
    override func setUpWithError() throws {
        calculator = Calculator()
    }
    
    override func tearDownWithError() throws {
        calculator = nil
    }
    
    func testAddition() throws {
        XCTAssertEqual(calculator.add(2, 3), 5)
        XCTAssertEqual(calculator.add(-1, 1), 0)
        XCTAssertEqual(calculator.add(0, 0), 0)
    }
    
    func testSubtraction() throws {
        XCTAssertEqual(calculator.subtract(5, 3), 2)
        XCTAssertEqual(calculator.subtract(1, 1), 0)
        XCTAssertEqual(calculator.subtract(0, 5), -5)
    }
    
    func testMultiplication() throws {
        XCTAssertEqual(calculator.multiply(3, 4), 12)
        XCTAssertEqual(calculator.multiply(-2, 5), -10)
        XCTAssertEqual(calculator.multiply(0, 100), 0)
    }
    
    func testDivision() throws {
        let result = try calculator.divide(10, 2)
        XCTAssertEqual(result, 5.0, accuracy: 0.001)
        
        let negativeResult = try calculator.divide(-10, 2)
        XCTAssertEqual(negativeResult, -5.0, accuracy: 0.001)
    }
    
    func testDivisionByZero() throws {
        XCTAssertThrowsError(try calculator.divide(5, 0)) { error in
            XCTAssertTrue(error is CalculatorError)
            if case CalculatorError.divisionByZero = error {
                // Expected error
            } else {
                XCTFail("Expected CalculatorError.divisionByZero")
            }
        }
    }
    
    func testFactorial() throws {
        XCTAssertEqual(try calculator.factorial(0), 1)
        XCTAssertEqual(try calculator.factorial(1), 1)
        XCTAssertEqual(try calculator.factorial(5), 120)
        
        XCTAssertThrowsError(try calculator.factorial(-1)) { error in
            XCTAssertTrue(error is CalculatorError)
        }
    }
}