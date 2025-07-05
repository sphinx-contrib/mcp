from sphinx_mcp.main import main as sphinx_mcp_main, MSG_PLACEHOLDER


class TestMain:
    def test_main(self):
        """Test the main function."""
        response = sphinx_mcp_main()
        assert response == MSG_PLACEHOLDER, (
            "Main function did not return the expected placeholder message."
        )
