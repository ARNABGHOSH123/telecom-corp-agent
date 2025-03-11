from services.multi_agent_service import app

if __name__ == "__main__":
    try:
        graph = app.get_graph().draw_mermaid_png()  # Generate the PNG
        with open("multi_agent_graph.png", "wb") as f:
            f.write(graph)  # Save it manually
        print("Graph saved as multi_agent_graph.png")
    except Exception as e:
        print(f"Error generating graph: {e}")

