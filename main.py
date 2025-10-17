"""
Main Program for ABC Theory Computational Examples

This program demonstrates all four advanced number theory and geometry theories
with their simplest computable examples:
1. p-adic Teichmüller Theory - Tate curves
2. Anabelian Geometry - Belyi maps and monodromy
3. Arakelov/Hodge Theory - Height computations
4. Frobenioid Theory - Monoid examples
"""

import sys
import time
from p_adic_teichmuller import demonstrate_tate_curve
from anabelian_geometry import demonstrate_anabelian_geometry
from arakelov_hodge import demonstrate_arakelov_hodge
from frobenioid import demonstrate_frobenioid


def print_header():
    """Print program header."""
    print("=" * 80)
    print("ABC Theory Computational Examples")
    print("最簡可計算範例：p-adic Teichmüller, Anabelian Geometry, Arakelov/Hodge, Frobenioid")
    print("=" * 80)
    print()


def print_section_header(title, section_num):
    """Print section header."""
    print("\n" + "=" * 60)
    print(f"{section_num}. {title}")
    print("=" * 60)


def interactive_menu():
    """Interactive menu for selecting demonstrations."""
    while True:
        print("\n" + "=" * 50)
        print("選擇要執行的範例 (Select Example to Run):")
        print("=" * 50)
        print("1. p-adic Teichmüller Theory - Tate Curves")
        print("2. Anabelian Geometry - Belyi Maps and Monodromy")
        print("3. Arakelov/Hodge Theory - Height Computations")
        print("4. Frobenioid Theory - Monoid Examples")
        print("5. 執行所有範例 (Run All Examples)")
        print("0. 退出 (Exit)")
        print("-" * 50)
        
        try:
            choice = input("請輸入選擇 (Enter choice): ").strip()
            
            if choice == '0':
                print("感謝使用！(Thank you for using!)")
                break
            elif choice == '1':
                print_section_header("p-adic Teichmüller Theory - Tate Curves", 1)
                demonstrate_tate_curve()
            elif choice == '2':
                print_section_header("Anabelian Geometry - Belyi Maps and Monodromy", 2)
                demonstrate_anabelian_geometry()
            elif choice == '3':
                print_section_header("Arakelov/Hodge Theory - Height Computations", 3)
                demonstrate_arakelov_hodge()
            elif choice == '4':
                print_section_header("Frobenioid Theory - Monoid Examples", 4)
                demonstrate_frobenioid()
            elif choice == '5':
                run_all_examples()
            else:
                print("無效選擇，請重新輸入 (Invalid choice, please try again)")
                
        except KeyboardInterrupt:
            print("\n\n程式被中斷 (Program interrupted)")
            break
        except Exception as e:
            print(f"發生錯誤 (Error occurred): {e}")


def run_all_examples():
    """Run all examples sequentially."""
    print_header()
    
    examples = [
        ("p-adic Teichmüller Theory - Tate Curves", demonstrate_tate_curve),
        ("Anabelian Geometry - Belyi Maps and Monodromy", demonstrate_anabelian_geometry),
        ("Arakelov/Hodge Theory - Height Computations", demonstrate_arakelov_hodge),
        ("Frobenioid Theory - Monoid Examples", demonstrate_frobenioid),
    ]
    
    for i, (title, demo_func) in enumerate(examples, 1):
        print_section_header(title, i)
        
        try:
            start_time = time.time()
            demo_func()
            end_time = time.time()
            
            print(f"\n範例 {i} 執行完成 (Example {i} completed)")
            print(f"執行時間 (Execution time): {end_time - start_time:.2f} 秒")
            
            if i < len(examples):
                input("\n按 Enter 繼續下一個範例 (Press Enter to continue)...")
                
        except Exception as e:
            print(f"範例 {i} 執行時發生錯誤 (Error in example {i}): {e}")
            continue
    
    print("\n" + "=" * 60)
    print("所有範例執行完成！(All examples completed!)")
    print("=" * 60)


def main():
    """Main program entry point."""
    if len(sys.argv) > 1:
        # Command line argument provided
        if sys.argv[1] == '--all':
            run_all_examples()
        elif sys.argv[1] == '--interactive':
            interactive_menu()
        else:
            print("用法 (Usage):")
            print("  python main.py              # 互動式選單 (Interactive menu)")
            print("  python main.py --all         # 執行所有範例 (Run all examples)")
            print("  python main.py --interactive # 互動式選單 (Interactive menu)")
    else:
        # Default: interactive menu
        interactive_menu()


if __name__ == "__main__":
    main()
