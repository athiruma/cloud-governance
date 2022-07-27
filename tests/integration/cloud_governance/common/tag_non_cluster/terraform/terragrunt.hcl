terraform {

    source = "./module/aws_instance//."

    before_hook "generate_tfvars" {
      commands     = ["apply", "plan"]
      execute      = ["python3", "tfvars_generator.py"]
    } 

    extra_arguments "common_vars"{
      commands = ["plan", "apply", "destroy"]

      arguments = [
        "-var-file=./input_vars.tfvars"
      ]
    }
}

generate "provider" {
  path = "provider.tf"
  if_exists = "overwrite_terragrunt"
  contents = <<EOF
provider "aws" {
  region = var.region_name
  assume_role {
    role_arn = "arn:aws:iam::$${var.account_id}:role/$${var.role_name}"
  }
}
EOF
}
