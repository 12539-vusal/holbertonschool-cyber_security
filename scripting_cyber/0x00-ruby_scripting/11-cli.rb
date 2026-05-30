#!/usr/bin/env ruby
require 'optparse'

TASKS_FILE = 'tasks.txt'

def load_tasks
  File.exist?(TASKS_FILE) ? File.readlines(TASKS_FILE, chomp: true) : []
end

def save_tasks(tasks)
  File.write(TASKS_FILE, tasks.join("\n") + (tasks.empty? ? "" : "\n"))
end

options = {}
parser = OptionParser.new do |opts|
  opts.banner = "Usage: cli.rb [options]"
  opts.on('-a', '--add TASK', 'Add a new task') { |t| options[:add] = t }
  opts.on('-l', '--list', 'List all tasks') { options[:list] = true }
  opts.on('-r', '--remove INDEX', 'Remove a task by index') { |i| options[:remove] = i.to_i }
  opts.on('-h', '--help', 'Show help') { puts opts; exit }
end

parser.parse!

if options[:add]
  tasks = load_tasks
  tasks << options[:add]
  save_tasks(tasks)
  puts "Task '#{options[:add]}' added."
elsif options[:list]
  tasks = load_tasks
  tasks.each_with_index { |t, i| puts "#{i + 1}. #{t}" }
elsif options[:remove]
  tasks = load_tasks
  idx = options[:remove] - 1
  removed = tasks.delete_at(idx)
  save_tasks(tasks)
  puts "Task '#{removed}' removed."
end
