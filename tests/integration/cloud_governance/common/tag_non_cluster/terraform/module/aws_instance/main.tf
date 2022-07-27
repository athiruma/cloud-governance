
resource "aws_instance" "main" {
  for_each = var.input_variables
  instance_type = each.value.instance_type 
  ami = each.value.image_name
  tags = {
      Name = each.value.tag_name
  }
}
