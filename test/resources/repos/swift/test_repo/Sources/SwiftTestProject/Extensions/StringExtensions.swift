import Foundation

/// Useful extensions for String type
public extension String {
    
    /// Capitalizes the first letter of the string
    /// - Returns: String with first letter capitalized
    func capitalizeFirstLetter() -> String {
        return prefix(1).capitalized + dropFirst()
    }
    
    /// Checks if string is a valid email format
    /// - Returns: true if string matches email pattern
    var isValidEmail: Bool {
        let emailRegex = #"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"#
        let emailPredicate = NSPredicate(format: "SELF MATCHES %@", emailRegex)
        return emailPredicate.evaluate(with: self)
    }
    
    /// Removes whitespace and newlines from both ends
    /// - Returns: Trimmed string
    var trimmed: String {
        return trimmingCharacters(in: .whitespacesAndNewlines)
    }
    
    /// Converts string to camelCase
    /// - Returns: camelCase version of the string
    var camelCased: String {
        let components = self.components(separatedBy: .whitespacesAndPunctuationCharacters)
        let filtered = components.filter { !$0.isEmpty }
        
        guard !filtered.isEmpty else { return "" }
        
        let first = filtered[0].lowercased()
        let rest = filtered.dropFirst().map { $0.capitalizeFirstLetter() }
        
        return ([first] + rest).joined()
    }
    
    /// Returns the number of words in the string
    /// - Returns: Word count
    var wordCount: Int {
        let words = self.components(separatedBy: .whitespacesAndPunctuationCharacters)
        return words.filter { !$0.isEmpty }.count
    }
}