from PyQt6.QtWidgets import QApplication
import sys
from src.core.physics import Body, rk4_step

def console_test():
    bodies = [
        Body(100, [0, 100, 0], [10, 0, 0]),
        Body(102, [100, 0, 0], [12, 0, 0]),
        Body(104, [0, 0, 100], [14, 0, 0])
    ]
    print("Initial positions:")
    for i, body in enumerate(bodies):
        print(f"Body {i}: pos={body.pos}")
    for step in range(10):
        rk4_step(bodies, 0.01)
    print("\nAfter 10 steps:")
    for i, body in enumerate(bodies):
        print(f"Body {i}: pos={body.pos}")

def main():
    console_test()
    app = QApplication(sys.argv)
    from src.ui.main_window import MainWindow
    bodies = [
        Body(100, [0, 100, 0], [10, 0, 0]),
        Body(102, [100, 0, 0], [12, 0, 0]),
        Body(104, [0, 0, 100], [14, 0, 0])
    ]
    window = MainWindow(bodies)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
