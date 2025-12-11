{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    systems.url = "github:nix-systems/default";

    devenv = {
      url = "github:cachix/devenv";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = {
    self,
    nixpkgs,
    devenv,
    systems,
    ...
  } @ inputs: let
    forEachSystem = nixpkgs.lib.genAttrs (import systems);
  in {
    packages = forEachSystem (system: {
      devenv-up = self.devShells.${system}.default.config.procfileScript;
      devenv-test = self.devShells.${system}.default.config.test;
    });

    formatter = forEachSystem (system: nixpkgs.legacyPackages.${system}.alejandra);

    devShells =
      forEachSystem
      (system: let
        pkgs = import nixpkgs {
          inherit system;
        };
      in {
        default = devenv.lib.mkShell {
          inherit inputs pkgs;
          modules = [
            {
              packages = with pkgs; [
                graphviz-nox
                libz
              ];

              env.NIX_LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath (with pkgs; [
                gcc-unwrapped
                libz
              ]);

              env.LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath (with pkgs; [
                gcc-unwrapped
                libz
              ]);

              env.MPLBACKEND = "TkAgg";

              languages.python = {
                enable = true;

                package = pkgs.python313;
                # .withPackages (python-pkgs: with python-pkgs; [
                #     tkinter
                # ]);

                poetry = {
                  enable = true;
                  activate.enable = true;
                  install.enable = true;
                };

                libraries = with pkgs; [
                  graphviz-nox
                  libz
                ];
              };
            }
          ];
        };
      });
  };
}
