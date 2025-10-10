import sys
from generate_page import move_assets, generate_pages_recursive


def main():
    if len(sys.argv) < 2:
        basepath = "/"
    else:
        basepath = sys.argv[1]

    static_src = "static"
    from_path = "content"
    template_path = "template.html"
    dest_path = "docs"
    try:
        move_assets(static_src, dest_path)
        generate_pages_recursive(from_path, template_path, dest_path, basepath)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
