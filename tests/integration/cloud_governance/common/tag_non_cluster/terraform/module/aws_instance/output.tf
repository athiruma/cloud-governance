output "instance_id" {
  value = aws_instance.main.*.instance_details.id[0]
}
