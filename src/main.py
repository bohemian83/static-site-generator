from generate_page import move_assets, generate_pages_recursive


def main():
    static_src = "static"
    public_dest = "public"
    from_path = "content"
    template_path = "template.html"
    dest_path = "public"
    try:
        move_assets(static_src, public_dest)
        generate_pages_recursive(from_path, template_path, dest_path)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
