"""
GUI for the Python Project Generator.
A standalone application for creating Python projects from templates.
"""

import sys
import os
import threading
from pathlib import Path
from typing import Dict, Any, Optional

try:
    import wx
    import wx.lib.scrolledpanel as scrolled
    WX_AVAILABLE = True
except ImportError:
    wx = None
    scrolled = None
    WX_AVAILABLE = False

from project_generator import ProjectGenerator, TemplateManager, setup_logging

__version__ = "1.0.0"


if WX_AVAILABLE:
    class ProjectGeneratorFrame(wx.Frame):
        """Main frame for the project generator GUI."""
        
        def __init__(self):
            super().__init__(
                None,
                title=f"Python Project Generator v{__version__}",
                size=(950, 750)
            )
            
            self.generator = ProjectGenerator()
            self.template_manager = TemplateManager()
            self.setup_ui()
            self.setup_menubar()
            self.setup_statusbar()
            self.center_on_screen()
            
        def setup_ui(self):
            """Set up the user interface."""
            # Create main panel with notebook for tabs
            self.panel = wx.Panel(self)
            main_sizer = wx.BoxSizer(wx.VERTICAL)
            
            # Title
            title_label = wx.StaticText(
                self.panel,
                label="Python Project Generator",
                style=wx.ALIGN_CENTER
            )
            title_font = title_label.GetFont()
            title_font.SetPointSize(18)
            title_font.SetWeight(wx.FONTWEIGHT_BOLD)
            title_label.SetFont(title_font)
            
            # Create notebook for different sections
            self.notebook = wx.Notebook(self.panel)
            
            # Template Selection Tab
            self.template_panel = self.create_template_selection_panel()
            self.notebook.AddPage(self.template_panel, "Template")
            
            # Project Info Tab
            self.info_panel = self.create_project_info_panel()
            self.notebook.AddPage(self.info_panel, "Project Info")
            
            # Features Tab
            self.features_panel = self.create_features_panel()
            self.notebook.AddPage(self.features_panel, "Features")
            
            # Output Tab
            self.output_panel = self.create_output_panel()
            self.notebook.AddPage(self.output_panel, "Output")
            
            # Buttons
            button_sizer = wx.BoxSizer(wx.HORIZONTAL)
            
            self.preview_button = wx.Button(self.panel, label="Preview Structure")
            self.generate_button = wx.Button(self.panel, label="Generate Project")
            self.clear_button = wx.Button(self.panel, label="Clear Form")
            
            button_sizer.Add(self.preview_button, 0, wx.ALL, 5)
            button_sizer.Add(self.generate_button, 0, wx.ALL, 5)
            button_sizer.Add(self.clear_button, 0, wx.ALL, 5)
            
            # Layout
            main_sizer.Add(title_label, 0, wx.ALL | wx.CENTER, 10)
            main_sizer.Add(self.notebook, 1, wx.ALL | wx.EXPAND, 5)
            main_sizer.Add(button_sizer, 0, wx.ALL | wx.CENTER, 10)
            
            self.panel.SetSizer(main_sizer)
            
            # Bind events
            self.preview_button.Bind(wx.EVT_BUTTON, self.on_preview)
            self.generate_button.Bind(wx.EVT_BUTTON, self.on_generate)
            self.clear_button.Bind(wx.EVT_BUTTON, self.on_clear)
        
        def create_template_selection_panel(self):
            """Create the template selection panel."""
            panel = wx.Panel(self.notebook)
            sizer = wx.BoxSizer(wx.VERTICAL)
            
            # Template selection
            template_label = wx.StaticText(panel, label="Choose Project Template:")
            template_font = template_label.GetFont()
            template_font.SetWeight(wx.FONTWEIGHT_BOLD)
            template_label.SetFont(template_font)
            
            templates = self.template_manager.get_available_templates()
            template_choices = []
            self.template_ids = []
            
            for template_id, template_info in templates.items():
                choice_text = f"{template_info['name']} - {template_info['description']}"
                template_choices.append(choice_text)
                self.template_ids.append(template_id)
            
            self.template_choice = wx.Choice(panel, choices=template_choices)
            self.template_choice.SetSelection(0)  # Default to first template
            self.template_choice.Bind(wx.EVT_CHOICE, self.on_template_changed)
            
            # Template description
            self.template_desc = wx.StaticText(panel, label="")
            self.template_desc.Wrap(500)
            
            # Update description for default selection
            self.on_template_changed(None)
            
            # Layout
            sizer.Add(template_label, 0, wx.ALL, 10)
            sizer.Add(self.template_choice, 0, wx.ALL | wx.EXPAND, 10)
            sizer.Add(wx.StaticText(panel, label="Description:"), 0, wx.ALL, 10)
            sizer.Add(self.template_desc, 0, wx.ALL, 10)
            
            panel.SetSizer(sizer)
            return panel
        
        def create_project_info_panel(self):
            """Create the project information panel."""
            panel = scrolled.ScrolledPanel(self.notebook)
            panel.SetupScrolling()
            
            sizer = wx.BoxSizer(wx.VERTICAL)
            
            # Project Name
            name_sizer = wx.BoxSizer(wx.HORIZONTAL)
            name_label = wx.StaticText(panel, label="Project Name:")
            name_label.SetMinSize((120, -1))
            self.name_ctrl = wx.TextCtrl(panel, size=(300, -1))
            self.name_ctrl.SetToolTip("Enter the name of your Python project")
            name_sizer.Add(name_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
            name_sizer.Add(self.name_ctrl, 1, wx.ALL | wx.EXPAND, 5)
            
            # Description
            desc_sizer = wx.BoxSizer(wx.HORIZONTAL)
            desc_label = wx.StaticText(panel, label="Description:")
            desc_label.SetMinSize((120, -1))
            self.desc_ctrl = wx.TextCtrl(panel, style=wx.TE_MULTILINE, size=(300, 60))
            self.desc_ctrl.SetToolTip("Brief description of your project")
            desc_sizer.Add(desc_label, 0, wx.ALL | wx.ALIGN_TOP, 5)
            desc_sizer.Add(self.desc_ctrl, 1, wx.ALL | wx.EXPAND, 5)
            
            # Author
            author_sizer = wx.BoxSizer(wx.HORIZONTAL)
            author_label = wx.StaticText(panel, label="Author:")
            author_label.SetMinSize((120, -1))
            self.author_ctrl = wx.TextCtrl(panel, size=(300, -1))
            self.author_ctrl.SetToolTip("Your name")
            author_sizer.Add(author_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
            author_sizer.Add(self.author_ctrl, 1, wx.ALL | wx.EXPAND, 5)
            
            # Email
            email_sizer = wx.BoxSizer(wx.HORIZONTAL)
            email_label = wx.StaticText(panel, label="Email:")
            email_label.SetMinSize((120, -1))
            self.email_ctrl = wx.TextCtrl(panel, size=(300, -1))
            self.email_ctrl.SetToolTip("Your email address")
            email_sizer.Add(email_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
            email_sizer.Add(self.email_ctrl, 1, wx.ALL | wx.EXPAND, 5)
            
            # Version
            version_sizer = wx.BoxSizer(wx.HORIZONTAL)
            version_label = wx.StaticText(panel, label="Version:")
            version_label.SetMinSize((120, -1))
            self.version_ctrl = wx.TextCtrl(panel, value="0.1.0", size=(300, -1))
            self.version_ctrl.SetToolTip("Initial version number")
            version_sizer.Add(version_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
            version_sizer.Add(self.version_ctrl, 1, wx.ALL | wx.EXPAND, 5)
            
            # URL
            url_sizer = wx.BoxSizer(wx.HORIZONTAL)
            url_label = wx.StaticText(panel, label="URL:")
            url_label.SetMinSize((120, -1))
            self.url_ctrl = wx.TextCtrl(panel, size=(300, -1))
            self.url_ctrl.SetToolTip("Project homepage or repository URL")
            url_sizer.Add(url_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
            url_sizer.Add(self.url_ctrl, 1, wx.ALL | wx.EXPAND, 5)
            
            # License Type
            license_sizer = wx.BoxSizer(wx.HORIZONTAL)
            license_label = wx.StaticText(panel, label="License:")
            license_label.SetMinSize((120, -1))
            license_choices = ["MIT", "Apache-2.0", "GPL-3.0", "BSD-3-Clause", "Custom"]
            self.license_ctrl = wx.Choice(panel, choices=license_choices)
            self.license_ctrl.SetSelection(0)  # Default to MIT
            self.license_ctrl.SetToolTip("Choose a license for your project")
            license_sizer.Add(license_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
            license_sizer.Add(self.license_ctrl, 1, wx.ALL | wx.EXPAND, 5)
            
            # Output Directory
            output_sizer = wx.BoxSizer(wx.HORIZONTAL)
            output_label = wx.StaticText(panel, label="Output Dir:")
            output_label.SetMinSize((120, -1))
            self.output_ctrl = wx.TextCtrl(panel, value=str(Path.home() / "Projects"), size=(250, -1))
            self.output_browse = wx.Button(panel, label="Browse...", size=(80, -1))
            self.output_browse.Bind(wx.EVT_BUTTON, self.on_browse_output)
            output_sizer.Add(output_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
            output_sizer.Add(self.output_ctrl, 1, wx.ALL | wx.EXPAND, 5)
            output_sizer.Add(self.output_browse, 0, wx.ALL, 5)
            
            # Add all to main sizer
            sizer.Add(name_sizer, 0, wx.ALL | wx.EXPAND, 5)
            sizer.Add(desc_sizer, 0, wx.ALL | wx.EXPAND, 5)
            sizer.Add(author_sizer, 0, wx.ALL | wx.EXPAND, 5)
            sizer.Add(email_sizer, 0, wx.ALL | wx.EXPAND, 5)
            sizer.Add(version_sizer, 0, wx.ALL | wx.EXPAND, 5)
            sizer.Add(url_sizer, 0, wx.ALL | wx.EXPAND, 5)
            sizer.Add(license_sizer, 0, wx.ALL | wx.EXPAND, 5)
            sizer.Add(output_sizer, 0, wx.ALL | wx.EXPAND, 5)
            
            panel.SetSizer(sizer)
            return panel
            
        def create_features_panel(self):
            """Create the features selection panel."""
            panel = scrolled.ScrolledPanel(self.notebook)
            panel.SetupScrolling()
            
            sizer = wx.BoxSizer(wx.VERTICAL)
            
            # Create feature checkboxes
            self.feature_checkboxes = {}
            
            features = [
                ("cli", "Command Line Interface (CLI)", True, "Add a CLI with argument parsing"),
                ("gui", "Graphical User Interface (GUI)", False, "Add a wxPython-based GUI"),
                ("tests", "Unit Tests", True, "Include pytest test framework"),
                ("executable", "Executable Building", False, "Add PyInstaller scripts for creating executables"),
                ("pypi_packaging", "PyPI Packaging", True, "Include setup.py and pyproject.toml for PyPI"),
                ("dev_requirements", "Development Requirements", True, "Include development dependencies"),
                ("license", "License File", True, "Include LICENSE file"),
                ("readme", "README.md", True, "Include comprehensive README file"),
                ("makefile", "Makefile", False, "Include Makefile for common tasks"),
                ("gitignore", ".gitignore", True, "Include .gitignore file"),
                ("github_actions", "GitHub Actions CI", False, "Include GitHub Actions workflow"),
            ]
            
            for feature_id, label, default, tooltip in features:
                checkbox = wx.CheckBox(panel, label=label)
                checkbox.SetValue(default)
                checkbox.SetToolTip(tooltip)
                self.feature_checkboxes[feature_id] = checkbox
                sizer.Add(checkbox, 0, wx.ALL, 5)
            
            # Add buttons for selecting all/none
            button_sizer = wx.BoxSizer(wx.HORIZONTAL)
            select_all_btn = wx.Button(panel, label="Select All")
            select_none_btn = wx.Button(panel, label="Select None")
            
            select_all_btn.Bind(wx.EVT_BUTTON, self.on_select_all)
            select_none_btn.Bind(wx.EVT_BUTTON, self.on_select_none)
            
            button_sizer.Add(select_all_btn, 0, wx.ALL, 5)
            button_sizer.Add(select_none_btn, 0, wx.ALL, 5)
            
            sizer.Add(wx.StaticLine(panel), 0, wx.ALL | wx.EXPAND, 10)
            sizer.Add(button_sizer, 0, wx.ALL | wx.CENTER, 5)
            
            panel.SetSizer(sizer)
            return panel
            
        def create_output_panel(self):
            """Create the output/log panel."""
            panel = wx.Panel(self.notebook)
            sizer = wx.BoxSizer(wx.VERTICAL)
            
            # Output text area
            self.output_text = wx.TextCtrl(
                panel,
                style=wx.TE_MULTILINE | wx.TE_READONLY,
                size=(-1, 400)
            )
            self.output_text.SetFont(wx.Font(9, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
            
            # Clear output button
            clear_output_btn = wx.Button(panel, label="Clear Output")
            clear_output_btn.Bind(wx.EVT_BUTTON, self.on_clear_output)
            
            sizer.Add(self.output_text, 1, wx.ALL | wx.EXPAND, 5)
            sizer.Add(clear_output_btn, 0, wx.ALL | wx.CENTER, 5)
            
            panel.SetSizer(sizer)
            return panel
        
        def setup_menubar(self):
            """Set up the menu bar."""
            menubar = wx.MenuBar()
            
            # File menu
            file_menu = wx.Menu()
            file_menu.Append(wx.ID_NEW, "New Project\tCtrl+N", "Start a new project")
            file_menu.AppendSeparator()
            file_menu.Append(wx.ID_EXIT, "Exit\tCtrl+Q", "Exit the application")
            menubar.Append(file_menu, "&File")
            
            # Templates menu
            templates_menu = wx.Menu()
            templates_menu.Append(wx.ID_REFRESH, "Refresh Templates\tF5", "Refresh template list")
            menubar.Append(templates_menu, "&Templates")
            
            # Help menu
            help_menu = wx.Menu()
            help_menu.Append(wx.ID_ABOUT, "About\tF1", "About this application")
            menubar.Append(help_menu, "&Help")
            
            self.SetMenuBar(menubar)
            
            # Bind menu events
            self.Bind(wx.EVT_MENU, self.on_clear, id=wx.ID_NEW)
            self.Bind(wx.EVT_MENU, self.on_exit, id=wx.ID_EXIT)
            self.Bind(wx.EVT_MENU, self.on_refresh_templates, id=wx.ID_REFRESH)
            self.Bind(wx.EVT_MENU, self.on_about, id=wx.ID_ABOUT)
        
        def setup_statusbar(self):
            """Set up the status bar."""
            self.statusbar = self.CreateStatusBar(2)
            self.statusbar.SetStatusText("Ready to generate projects", 0)
            self.statusbar.SetStatusText(f"v{__version__}", 1)
        
        def center_on_screen(self):
            """Center the window on the screen."""
            self.Center()
        
        def log_to_output(self, message: str):
            """Add a message to the output text area."""
            wx.CallAfter(self._append_to_output, message)
        
        def _append_to_output(self, message: str):
            """Append message to output (called from main thread)."""
            self.output_text.AppendText(f"{message}\n")
        
        def on_template_changed(self, event):
            """Handle template selection change."""
            if hasattr(self, 'template_choice'):
                selection = self.template_choice.GetSelection()
                if selection >= 0 and selection < len(self.template_ids):
                    template_id = self.template_ids[selection]
                    templates = self.template_manager.get_available_templates()
                    template_info = templates.get(template_id, {})
                    
                    description = template_info.get('description', 'No description available')
                    features = template_info.get('features', [])
                    
                    desc_text = f"{description}\n\nDefault features: {', '.join(features)}"
                    self.template_desc.SetLabel(desc_text)
                    self.template_desc.Wrap(500)
        
        def on_browse_output(self, event):
            """Handle browse output directory button."""
            with wx.DirDialog(self, "Choose output directory") as dialog:
                if dialog.ShowModal() == wx.ID_OK:
                    self.output_ctrl.SetValue(dialog.GetPath())
        
        def on_select_all(self, event):
            """Select all features."""
            for checkbox in self.feature_checkboxes.values():
                checkbox.SetValue(True)
        
        def on_select_none(self, event):
            """Deselect all features."""
            for checkbox in self.feature_checkboxes.values():
                checkbox.SetValue(False)
        
        def on_clear_output(self, event):
            """Clear the output text."""
            self.output_text.Clear()
        
        def on_refresh_templates(self, event):
            """Refresh the template list."""
            self.log_to_output("Refreshing templates...")
            # In a real implementation, this would refresh templates from remote sources
            self.log_to_output("Templates refreshed.")
        
        def on_preview(self, event):
            """Preview the project structure."""
            project_name = self.name_ctrl.GetValue().strip()
            if not project_name:
                wx.MessageBox("Please enter a project name", "Missing Information", wx.OK | wx.ICON_WARNING)
                return
            
            self.log_to_output(f"=== Project Structure Preview for '{project_name}' ===")
            self.log_to_output(f"Template: {self.get_selected_template()}")
            self.log_to_output("")
            
            features = self.get_selected_features()
            package_name = project_name.lower().replace('-', '_').replace(' ', '_')
            
            self.log_to_output(f"{project_name}/")
            self.log_to_output("├── src/")
            self.log_to_output(f"│   └── {package_name}/")
            self.log_to_output("│       ├── __init__.py")
            self.log_to_output("│       └── core.py")
            
            if features.get('cli'):
                self.log_to_output("│       ├── cli.py")
            if features.get('gui'):
                self.log_to_output("│       └── gui.py")
            
            if features.get('tests'):
                self.log_to_output("├── tests/")
                self.log_to_output("│   ├── __init__.py")
                self.log_to_output("│   └── test_core.py")
            
            if features.get('pypi_packaging'):
                self.log_to_output("├── setup.py")
                self.log_to_output("└── requirements.txt")
            
            if features.get('readme'):
                self.log_to_output("├── README.md")
            
            if features.get('license'):
                self.log_to_output("├── LICENSE")
            
            if features.get('gitignore'):
                self.log_to_output("├── .gitignore")
            
            self.log_to_output("")
            self.log_to_output("=== End Preview ===")
            self.log_to_output("")
        
        def on_generate(self, event):
            """Generate the project."""
            # Validate input
            project_name = self.name_ctrl.GetValue().strip()
            if not project_name:
                wx.MessageBox("Please enter a project name", "Missing Information", wx.OK | wx.ICON_WARNING)
                return
            
            output_dir = Path(self.output_ctrl.GetValue().strip())
            if not output_dir.exists():
                wx.MessageBox("Output directory does not exist", "Invalid Directory", wx.OK | wx.ICON_ERROR)
                return
            
            # Check if project directory already exists
            project_path = output_dir / project_name
            if project_path.exists():
                result = wx.MessageBox(
                    f"Directory '{project_path}' already exists. Continue anyway?",
                    "Directory Exists",
                    wx.YES_NO | wx.ICON_QUESTION
                )
                if result == wx.NO:
                    return
            
            # Disable generate button during generation
            self.generate_button.Enable(False)
            self.statusbar.SetStatusText("Generating project...", 0)
            
            # Run generation in separate thread
            def generate_project():
                try:
                    template_id = self.get_selected_template()
                    features = self.get_selected_features()
                    metadata = self.get_project_metadata()
                    
                    self.log_to_output(f"Starting generation of '{project_name}'...")
                    self.log_to_output(f"Template: {template_id}")
                    self.log_to_output(f"Output directory: {output_dir}")
                    self.log_to_output("")
                    
                    success = self.generator.generate_project(
                        project_name=project_name,
                        output_dir=output_dir,
                        template_id=template_id,
                        features=features,
                        metadata=metadata
                    )
                    
                    if success:
                        self.log_to_output("")
                        self.log_to_output("✅ Project generated successfully!")
                        self.log_to_output(f"📁 Location: {project_path}")
                        self.log_to_output("")
                        self.log_to_output("Next steps:")
                        self.log_to_output(f"  cd '{project_path}'")
                        if features.get('dev_requirements'):
                            self.log_to_output("  pip install -r requirements-dev.txt")
                        self.log_to_output("  pip install -e .")
                        
                        wx.CallAfter(
                            wx.MessageBox,
                            f"Project '{project_name}' generated successfully!\n\nLocation: {project_path}",
                            "Success",
                            wx.OK | wx.ICON_INFORMATION
                        )
                    else:
                        self.log_to_output("")
                        self.log_to_output("❌ Project generation failed!")
                        wx.CallAfter(
                            wx.MessageBox,
                            "Project generation failed. Check the output for details.",
                            "Error",
                            wx.OK | wx.ICON_ERROR
                        )
                
                except Exception as e:
                    self.log_to_output(f"❌ Error: {str(e)}")
                    wx.CallAfter(
                        wx.MessageBox,
                        f"An error occurred: {str(e)}",
                        "Error",
                        wx.OK | wx.ICON_ERROR
                    )
                finally:
                    wx.CallAfter(self.generate_button.Enable, True)
                    wx.CallAfter(self.statusbar.SetStatusText, "Ready to generate projects", 0)
            
            thread = threading.Thread(target=generate_project)
            thread.daemon = True
            thread.start()
        
        def on_clear(self, event):
            """Clear the form."""
            # Clear project info
            self.name_ctrl.Clear()
            self.desc_ctrl.Clear()
            self.author_ctrl.Clear()
            self.email_ctrl.Clear()
            self.version_ctrl.SetValue("0.1.0")
            self.url_ctrl.Clear()
            self.license_ctrl.SetSelection(0)
            self.output_ctrl.SetValue(str(Path.home() / "Projects"))
            
            # Reset template selection
            self.template_choice.SetSelection(0)
            self.on_template_changed(None)
            
            # Reset features to defaults
            defaults = {
                'cli': True, 'gui': False, 'tests': True, 'executable': False,
                'pypi_packaging': True, 'dev_requirements': True, 'license': True,
                'readme': True, 'makefile': False, 'gitignore': True, 'github_actions': False
            }
            
            for feature_id, checkbox in self.feature_checkboxes.items():
                checkbox.SetValue(defaults.get(feature_id, False))
            
            self.log_to_output("Form cleared.")
        
        def on_exit(self, event):
            """Handle exit menu item."""
            self.Close()
        
        def on_about(self, event):
            """Handle about menu item."""
            about_info = wx.adv.AboutDialogInfo()
            about_info.SetName("Python Project Generator")
            about_info.SetVersion(__version__)
            about_info.SetDescription(
                "A standalone GUI tool for generating customizable Python project skeletons.\n\n"
                "Features:\n"
                "• Multiple project templates\n"
                "• Customizable feature selection\n"
                "• Professional project structure\n"
                "• Ready for PyPI and development\n\n"
                "Create professional Python projects in seconds!"
            )
            about_info.SetCopyright("(C) 2024 Python Project Generator")
            about_info.AddDeveloper("Built with wxPython")
            
            wx.adv.AboutBox(about_info)
        
        def get_selected_template(self) -> str:
            """Get the selected template ID."""
            selection = self.template_choice.GetSelection()
            if selection >= 0 and selection < len(self.template_ids):
                return self.template_ids[selection]
            return "minimal-python"  # fallback
        
        def get_selected_features(self) -> Dict[str, bool]:
            """Get the selected features as a dictionary."""
            return {
                feature_id: checkbox.GetValue()
                for feature_id, checkbox in self.feature_checkboxes.items()
            }
        
        def get_project_metadata(self) -> Dict[str, str]:
            """Get the project metadata as a dictionary."""
            license_choices = ["MIT", "Apache-2.0", "GPL-3.0", "BSD-3-Clause", "Custom"]
            selected_license = license_choices[self.license_ctrl.GetSelection()]
            
            return {
                "description": self.desc_ctrl.GetValue().strip(),
                "author": self.author_ctrl.GetValue().strip(),
                "email": self.email_ctrl.GetValue().strip(),
                "version": self.version_ctrl.GetValue().strip(),
                "url": self.url_ctrl.GetValue().strip(),
                "license_type": selected_license,
            }


    class ProjectGeneratorApp(wx.App):
        """Main wxPython application class for the project generator."""
        
        def OnInit(self):
            """Initialize the application."""
            frame = ProjectGeneratorFrame()
            frame.Show()
            return True

else:
    # Dummy classes when wxPython is not available
    class ProjectGeneratorFrame:
        """Dummy frame class when wxPython is not available."""
        pass
    
    class ProjectGeneratorApp:
        """Dummy app class when wxPython is not available."""
        pass


def main() -> int:
    """
    Main entry point for the project generator GUI.
    
    Returns:
        Exit code (0 for success, non-zero for error)
    """
    if not WX_AVAILABLE:
        print("Error: wxPython is not installed.")
        print("Install it with: pip install wxpython")
        print("")
        print("On macOS, you might need to use:")
        print("  pip install -U wxpython")
        print("")
        print("On Linux, you might need to install system dependencies first:")
        print("  sudo apt-get install libgtk-3-dev libwebkitgtk-3.0-dev")
        print("  pip install wxpython")
        return 1
    
    setup_logging(level="INFO")
    
    app = ProjectGeneratorApp()
    app.MainLoop()
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 