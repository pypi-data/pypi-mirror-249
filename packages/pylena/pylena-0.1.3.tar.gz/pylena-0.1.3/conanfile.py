# pylint: skip-file
from conan import ConanFile
from conan.tools.build import check_min_cppstd
from conan.tools.cmake import CMakeToolchain, CMakeDeps, CMake
from conans.errors import ConanInvalidConfiguration


class PyleneNumpyConan(ConanFile):
    name = "pylene-numpy"
    version = "head"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True, "pylene/*:fPIC": True,
                       "onetbb/*:tbbproxy": False}
    exports_sources = "CMakeLists.txt", "pylene-numpy/*", "LICENCE"
    implements = ["auto_shared_fpic"]

    def requirements(self):
        self.requires("pylene/head@lrde/unstable", transitive_headers=True)
        self.requires("pybind11/2.9.2", transitive_headers=True)
        self.requires("libwebp/1.3.2", override=True)
        
    def validate(self):
        check_min_cppstd(self, 20)


    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")
        
        if not self.options.shared and self.options.get_safe("fPIC") == False:
            raise ConanInvalidConfiguration("pylene-numpy is intended to be linked to python module and should be compiled with fPIC")

    def validate(self):
        if self.dependencies["onetbb"].options.get_safe("tbbproxy") == True:            
            raise ConanInvalidConfiguration("llvmlite crashes when malloc is redirected to tbbmalloc with tbbproxy option. Use '-o onetbb:tbbproxy=False'")


    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()
        tc = CMakeToolchain(self)
        tc.generate()

    def layout(self):
        self.folders.source = "."
        self.folders.build = "build"
        self.folders.generators = "build"

        self.cpp.source.includedirs = ["pylene-numpy/include"]
        self.cpp.build.libdirs = ["pylene-numpy"]
        self.cpp.package.libdirs = ["lib"]
        self.cpp.package.includedirs = ["include"]

    def build(self):
        variables = {"BUILD_PYLENA": "OFF"}
        cmake = CMake(self)
        cmake.configure(variables)
        cmake.build()
        cmake.install()

    def package_info(self):
        self.cpp_info.set_property("cmake_target_name", "pylene-numpy::pylene-numpy")

        # Core pylene numpy
        self.cpp_info.requires = ["pylene::core", "pybind11::pybind11"]
        self.cpp_info.libs = ["pylene-numpy"]