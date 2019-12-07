from conans import ConanFile, CMake, tools
import os


class NvPipeConan(ConanFile):
    name = "nvpipe"
    version = "0.1"
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"

    options = {
        "with_encoder": [True, False],
        "with_decoder": [True, False],
        "with_opengl": [True, False],
    }

    default_options = (
        "with_encoder=True",
        "with_decoder=True",
        "with_opengl=True",
        )

    exports = ["CMakeLists.txt", "FindNvPipe.cmake"]

    url="http://github.com/ulricheck/conan-nvpipe"
    license="nvidia demo code - license unknown"
    description="NVIDIA-accelerated zero latency video compression library for interactive remoting applications"
    
    requires = (
        "cuda_dev_config/[>=1.0]@camposs/stable",
        )

    scm = {
        "type": "git",
        "subfolder": "sources",
        "url": "https://github.com/ulricheck/NvPipe.git",
        "revision": "master",
    }

    def build(self):
        """ Define your project building. You decide the way of building it
            to reuse it later in any other project.
        """
        cmake = CMake(self)

        cmake.definitions["NVPIPE_WITH_ENCODER"] = self.options.with_encoder
        cmake.definitions["NVPIPE_WITH_DECODER"] = self.options.with_decoder
        cmake.definitions["NVPIPE_WITH_OPENGL"] = self.options.with_opengl
        cmake.definitions["NVPIPE_BUILD_EXAMPLES"] = "OFF"
        cmake.definitions["CUDA_TOOLKIT_ROOT_DIR"] = self.options["cuda_dev_config"].cuda_root

        cmake.configure()
        cmake.build()
        cmake.install()

    def package(self):
        """ Define your conan structure: headers, libs, bins and data. After building your
            project, this method is called to create a defined structure:
        """
        # Copy findZLIB.cmake to package
        self.copy("FindNvPipe.cmake", ".", ".")
        
    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
