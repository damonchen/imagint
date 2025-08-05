import {
  ArrowDownIcon,
  ArrowRightIcon,
  ArrowUpIcon,
  CheckCircledIcon,
  CircleIcon,
  CrossCircledIcon,
  QuestionMarkCircledIcon,
  StopwatchIcon,
} from '@radix-ui/react-icons'

// should project
export const labels = [
  {
    value: 'bug',
    label: 'Bug',
  },
  {
    value: 'feature',
    label: 'Feature',
  },
  {
    value: 'documentation',
    label: 'Documentation',
  },
]

export const statuses = [
  {
    value: 'not_applied',
    label: 'NotApplied',
    icon: QuestionMarkCircledIcon,
  },
  {
    value: 'applied',
    label: 'Applied',
    icon: CircleIcon,
  },
  {
    value: 'rejected',
    label: 'Rejected',
    icon: StopwatchIcon,
  },
  {
    value: 'confirmed',
    label: 'Confirmed',
    icon: CheckCircledIcon,
  },
  {
    value: 'issued',
    label: 'Issued',
    icon: CrossCircledIcon,
  },
  {
    value: 'closed',
    label: 'Closed',
    icon: CrossCircledIcon,
  },
]

export const priorities = [
  {
    label: 'Low',
    value: 'low',
    icon: ArrowDownIcon,
  },
  {
    label: 'Medium',
    value: 'medium',
    icon: ArrowRightIcon,
  },
  {
    label: 'High',
    value: 'high',
    icon: ArrowUpIcon,
  },
]
