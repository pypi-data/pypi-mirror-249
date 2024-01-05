from nexatestlib import Multiplication

def test_multiplication():
    # Instantiate a Multiplication object
    multiplication = Multiplication(2)
    # Call the multiply method
    assert multiplication.multiply(5) == 10
    assert multiplication.multiply(10) == 20
    assert multiplication.multiply(0) == 0